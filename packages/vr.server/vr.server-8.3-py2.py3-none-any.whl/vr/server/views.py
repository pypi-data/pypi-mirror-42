import datetime
import json
import logging
import textwrap

from django.conf import settings
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import edit
from django.views.generic import ListView

# Imported as recommended in the low-level API docs:
# https://django-reversion.readthedocs.org/en/latest/api.html?#importing-the-low-level-api
import reversion as revisions
from reversion import create_revision

from reversion.helpers import generate_patch, generate_patch_html

from vr.server import forms, tasks, events, models
from vr.server.utils import yamlize, build_swarm_trace_id

logger = logging.getLogger('velociraptor')


VERSION_DIFFS_LIMIT = 10


def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except Exception:
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator


def app_in_default_dashboard(app, user):
    """
    Determines if an app is part of the user's default dashboard.
    """
    try:
        dashboard = user.userprofile.default_dashboard
    except ObjectDoesNotExist:
        return False
    return dashboard and app.id in dashboard.apps.values_list('id', flat=True)


@login_required
def dash(request):
    return render(request, 'dash.html', {
        'hosts': models.Host.objects.filter(active=True),
        'dashboard_id': '',
        'dashboard_name': 'Home',
        'supervisord_web_port': settings.SUPERVISORD_WEB_PORT
    })


@login_required
def default_dash(request):
    if hasattr(request.user, 'userprofile') and request.user.userprofile:
        dashboard = request.user.userprofile.default_dashboard
        if dashboard is not None:
            dashboard_name = 'Default - %s' % dashboard.name
            return render(request, 'dash.html', {
                'hosts': models.Host.objects.filter(active=True),
                'dashboard_id': dashboard.id,
                'dashboard_name': dashboard_name,
                'supervisord_web_port': settings.SUPERVISORD_WEB_PORT
            })
    # If you don't have a default dashboard go to home!
    return HttpResponseRedirect('/')


@login_required
def custom_dash(request, slug):
    dashboard = get_object_or_404(models.Dashboard, slug=slug)
    return render(request, 'dash.html', {
        'hosts': models.Host.objects.filter(active=True),
        'dashboard_id': dashboard.id,
        'dashboard_name': dashboard.name,
        'quick_dashboard': True,
        'supervisord_web_port': settings.SUPERVISORD_WEB_PORT
    })


@login_required
def build_app(request):
    form = forms.BuildForm(request.POST or None)
    if form.is_valid():
        app = models.App.objects.get(id=form.cleaned_data['app_id'])

        build = models.Build(app=app, tag=form.cleaned_data['tag'],
                             os_image=app.get_os_image())
        build.save()
        do_build(build, request.user)

        # If app is part of the user's default dashboard, redirect there.
        if app_in_default_dashboard(app, request.user):
            return redirect('default_dash')

        return redirect('dash')
    return render(request, 'basic_form.html', {
        'form': form,
        'btn_text': 'Build',
    })


def do_build(build, user):
    """
    Put a build job on the worker queue, and a notification about it on the
    pubsub.
    """
    tasks.build_app.delay(build_id=build.id)
    events.eventify(
        user, 'build', build,
        resource_uri='/admin/server/builds/{}/'.format(build.id))


@login_required
def upload_build(request):
    form = forms.BuildUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        events.eventify(request.user, 'upload', form.instance)
        return HttpResponseRedirect(reverse('deploy'))

    return render(request, 'basic_form.html', {
        'form': form,
        'btn_text': 'Upload',
        'instructions': """Use this form to upload a build.  A valid build
        should have a Procfile, and have all app-specific dependencies already
        compiled into the env.""",
        'enctype': "multipart/form-data"
    })


@login_required
def release(request):
    form = forms.ReleaseForm(request.POST or None)
    if form.is_valid():
        # Take the env vars from the build, update with vars from the form, and
        # save on the instance.
        release = form.instance
        env_yaml = release.build.env_yaml or {}
        env_yaml.update(release.env_yaml or {})
        release.env_yaml = env_yaml
        form.save()
        events.eventify(
            request.user, 'release', release,
            resource_uri='/admin/server/release/{}/'.format(release.id))
        return HttpResponseRedirect(reverse('deploy'))

    builds = models.Build.objects
    form.fields['build'].queryset = builds.filter(status=models.BUILD_SUCCESS)
    return render(request, 'basic_form.html', {
        'form': form,
        'btn_text': 'Save',
    })


@login_required
def deploy(request):
    # Construct the form for specifying deployments.
    form = forms.DeploymentForm(request.POST or None)

    if form.is_valid():
        # The form fields exactly match the arguments to the celery
        # task, so just use that dict for kwargs.
        data = form.cleaned_data

        release = models.Release.objects.get(id=data.pop('release_id'))
        if 'app' in data:
            data.pop('app')
        do_deploy(release, request.user, **data)

        # If app is part of the user's default dashboard, redirect there.
        if app_in_default_dashboard(release.build.app, request.user):
            return redirect('default_dash')

        return redirect('dash')

    return render(request, 'basic_form.html', vars())


def do_deploy(release, user, config_name, hostname, proc, port):
    """
    Put a deploy job on the work queue, and a notification about it on the
    events pubsub.
    """
    tasks.deploy.delay(release_id=release.id, config_name=config_name,
                       hostname=hostname, proc=proc, port=port)
    procname = '%(release)s-%(proc)s-%(port)s to %(hostname)s' % vars()
    events.eventify(
        user, 'deploy', procname,
        resource_uri='/admin/server/release/{}/'.format(release.id))


@login_required
def proclog(request, hostname, procname):
    return render(request, 'proclog.html', vars())


def _get_version_diffs_for_obj(obj, limit):
    version_list = revisions.get_for_object(obj)
    fields = [field for field in obj._meta.fields]
    version_diffs, last_edited = [], None
    if len(version_list) > 1:
        last_edited = version_list[0].revision.date_created
        old_versions = version_list[1:limit + 1]
        for iversion, version in enumerate(old_versions):
            newer_version = version_list[iversion]
            diff_dict = {}
            for field in fields:
                if generate_patch(version, newer_version, field.name):
                    # If versions differ, generate a pretty html diff
                    diff_html = generate_patch_html(
                        version, newer_version, field.name)
                    diff_dict[field.name] = (
                        version.field_dict[field.name],
                        newer_version.field_dict[field.name],
                        diff_html,
                    )
            version_diffs.append({
                'diff_dict': diff_dict,
                'user': newer_version.revision.user,
                'date': newer_version.revision.date_created,
            })
    return version_diffs, last_edited


@login_required
@revisions.create_revision()
def edit_swarm(request, swarm_id=None):
    if swarm_id:
        # Need to populate form from swarm
        swarm = get_object_or_404(models.Swarm, id=swarm_id)
        initial = {
            'app_id': swarm.app.id,
            'squad_id': swarm.squad.id,
            'tag': swarm.release.build.tag,
            'config_name': swarm.config_name,
            'config_yaml': yamlize(swarm.config_yaml),
            'env_yaml': yamlize(swarm.env_yaml),
            'volumes': yamlize(swarm.volumes),
            'run_as': swarm.run_as or 'nobody',
            'mem_limit': swarm.mem_limit,
            'memsw_limit': swarm.memsw_limit,
            'proc_name': swarm.proc_name,
            'size': swarm.size,
            'pool': swarm.pool or '',
            'balancer': swarm.balancer,
            'config_ingredients': [
                ing.pk for ing in swarm.config_ingredients.all()]
        }
        version_diffs, _last_edited = _get_version_diffs_for_obj(
            swarm, VERSION_DIFFS_LIMIT)
        compiled_config = yamlize(swarm.get_config())
        compiled_env = yamlize(swarm.get_env())

    else:
        initial = None
        swarm = models.Swarm()
        version_diffs = []
        compiled_config = yamlize({})
        compiled_env = yamlize({})

    form = forms.SwarmForm(request.POST or None, initial=initial)
    error_msg = None
    if form.is_valid():
        data = form.cleaned_data

        # Check if we already have a swarm with these parameters
        # Note: exclude itself, in case we are editing an existing swarm
        n = models.Swarm.objects.filter(
            app=data['app_id'],
            proc_name=data['proc_name'],
            config_name=data['config_name'],
            squad=data['squad_id'],
        ).exclude(id=swarm_id).count()

        if n > 0:
            error_msg = (
                'Swarm already exists for this app, proc, config and squad!'
            )

        else:
            swarm.app = models.App.objects.get(id=data['app_id'])
            swarm.squad = models.Squad.objects.get(id=data['squad_id'])
            swarm.config_name = data['config_name']
            swarm.config_yaml = data['config_yaml']
            swarm.env_yaml = data['env_yaml']
            swarm.volumes = data['volumes']
            swarm.run_as = data['run_as']
            swarm.mem_limit = data['mem_limit']
            swarm.memsw_limit = data['memsw_limit']
            swarm.proc_name = data['proc_name']
            swarm.size = data['size']
            swarm.pool = data['pool'] or None
            swarm.balancer = data['balancer'] or None
            swarm.release = swarm.get_current_release(data['tag'])
            swarm.save()
            swarm.config_ingredients.clear()
            for ingredient in data['config_ingredients']:
                swarm.config_ingredients.add(ingredient)

            # Set the version metadata as recommended in the low-level API docs
            # https://django-reversion.readthedocs.org/en/latest/api.html?#version-meta-data
            revisions.set_user(request.user)
            revisions.set_comment("Created from web form.")

            do_swarm(swarm, request.user)

            # If app is part of the user's default dashboard, redirect there.
            if app_in_default_dashboard(swarm.app, request.user):
                return redirect('default_dash')

            return redirect('dash')

    return render(request, 'swarm.html', {
        'swarm': swarm,
        'form': form,
        'error_msg': error_msg,
        'btn_text': 'Swarm',
        'version_diffs': version_diffs,
        'version_diffs_limit': VERSION_DIFFS_LIMIT,
        'compiled_config': compiled_config,
        'compiled_env': compiled_env
    })


@login_required
@json_response
def search_swarm(request):
    query = request.GET.get('query', None)

    if query:
        swarms = models.Swarm.objects.filter(
            Q(app__name__icontains=query) |
            Q(config_name__icontains=query) |
            Q(release__build__tag__icontains=query) |
            Q(proc_name__icontains=query))
    else:
        swarms = models.Swarm.objects.all()

    return [{
        'shortname': swarm.shortname(),
        'id': swarm.id,
        'app_name': swarm.app.name
    } for swarm in swarms]


def do_swarm(swarm, user):
    """
    Put a swarming job on the queue, and a notification about it on the pubsub.
    """
    # Create a swarm trace id that takes our swarm and time
    swarm_trace_id = build_swarm_trace_id(swarm)
    values = dict(
        user=user.username,
        shortname=swarm.shortname(),
        app=swarm.app,
        tag=swarm.release.build.tag,
        config_name=swarm.config_name,
        proc_name=swarm.proc_name,
        squad=swarm.squad,
        memory=swarm.get_memory_limit_str(),
        size=swarm.size,
        balancer=swarm.balancer,
        pool=swarm.pool,
        trace_id=swarm_trace_id,
    )
    ev_detail = textwrap.dedent(
        """%(user)s swarmed %(shortname)s

        App: %(app)s
        Version: %(tag)s
        Config Name: %(config_name)s
        Proc Name: %(proc_name)s
        Squad: %(squad)s
        Memory: %(memory)s
        Size: %(size)s
        Balancer: %(balancer)s
        Pool: %(pool)s
        Trace ID: %(trace_id)s
        """) % values
    events.eventify(
        user, 'swarm', swarm.shortname(),
        detail=ev_detail, swarm_id=swarm_trace_id,
        resource_uri='/swarm/{}/'.format(swarm.id))
    tasks.swarm_start.delay(swarm.id, swarm_trace_id)
    return swarm_trace_id


class ListLogEntry(ListView):
    template_name = 'log.html'
    model = models.DeploymentLogEntry
    paginate_by = 50
    query_params = {}

    def get_queryset(self):
        self.query_params = {
            k: v for k, v in self.request.GET.items()
            if k != 'page' and v.strip()
        }
        return models.DeploymentLogEntry.objects.filter(**self.query_params)

    def get_context_data(self, **kwargs):
        context = super(ListLogEntry, self).get_context_data(**kwargs)
        context['apps_list'] = models.App.objects.order_by(Lower('name'))
        context['users_list'] = User.objects.order_by(Lower('username'))
        context['q'] = self.query_params
        return context


class UpdateConfigIngredient(edit.UpdateView):
    template_name = 'ingredient_form.html'
    model = models.ConfigIngredient
    success_url = reverse_lazy('ingredient_list')
    form_class = forms.ConfigIngredientForm

    def get_context_data(self, **kwargs):
        """
        Augment the data passed to the template with:
        - version_diffs: Version history
        - last_edited: Last time when the ingredient was modified
        - related swarms
        """
        context = super(UpdateConfigIngredient, self).get_context_data(
            **kwargs)
        version_diffs, last_edited = _get_version_diffs_for_obj(
            self.object, VERSION_DIFFS_LIMIT)
        context['version_diffs'] = version_diffs
        context['version_diffs_limit'] = VERSION_DIFFS_LIMIT
        context['last_edited'] = last_edited or 'No data'
        context['related_swarms'] = self.object.swarm_set.all()
        return context

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Updated from web form.")
            return_value = super(UpdateConfigIngredient, self).form_valid(form)
        return return_value


class AddConfigIngredient(edit.CreateView):
    template_name = 'ingredient_form.html'
    model = models.ConfigIngredient
    success_url = reverse_lazy('ingredient_list')
    form_class = forms.ConfigIngredientForm

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Added from web form.")
            return_value = super(AddConfigIngredient, self).form_valid(form)
        return return_value


class ListConfigIngredient(ListView):
    template_name = 'ingredient_list.html'
    model = models.ConfigIngredient
    paginate_by = 30


class DeleteConfigIngredient(edit.DeleteView):
    model = models.ConfigIngredient
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('ingredient_list')

    def delete(self, request, *args, **kwargs):
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Deleted from web form.")
            return super(DeleteConfigIngredient, self).delete(request)


class ListHost(ListView):
    model = models.Host
    template_name = 'host_list.html'


class AddHost(edit.CreateView):
    template_name = 'host_form.html'
    model = models.Host
    success_url = reverse_lazy('host_list')
    form_class = forms.HostForm

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Added from web form.")
            return_value = super(AddHost, self).form_valid(form)
        return return_value


class UpdateHost(edit.UpdateView):
    template_name = 'host_form.html'
    model = models.Host
    success_url = reverse_lazy('host_list')
    form_class = forms.HostForm
    slug_field = 'name'

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Updated from web form.")
            return_value = super(UpdateHost, self).form_valid(form)
        return return_value


class DeleteHost(edit.DeleteView):
    model = models.Host
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('host_list')

    def delete(self, request, *args, **kwargs):
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Deleted from web form.")
            return super(DeleteHost, self).delete(request)


class ListSquad(ListView):
    model = models.Squad
    template_name = 'squad_list.html'


class AddSquad(edit.CreateView):
    template_name = 'squad_form.html'
    model = models.Squad
    success_url = reverse_lazy('squad_list')
    form_class = forms.SquadForm

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Added from web form.")
            return_value = super(AddSquad, self).form_valid(form)
        return return_value


class UpdateSquad(edit.UpdateView):
    template_name = 'squad_form.html'
    model = models.Squad
    success_url = reverse_lazy('squad_list')
    form_class = forms.SquadForm

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Updated from web form.")
            return_value = super(UpdateSquad, self).form_valid(form)
        return return_value


class DeleteSquad(edit.DeleteView):
    model = models.Squad
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('squad_list')

    def delete(self, request, *args, **kwargs):
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Deleted from web form.")
            return super(DeleteSquad, self).delete(request)


class ListApp(ListView):
    model = models.App
    template_name = 'app_list.html'


class AddApp(edit.CreateView):
    template_name = 'app_form.html'
    model = models.App
    success_url = reverse_lazy('app_list')

    # Get rid of the following message:
    # Using ModelFormMixin (base class of AddBuildPack) without the 'fields'
    # attribute is prohibited.
    fields = ['name', 'repo_url', 'repo_type', 'buildpack', 'stack']

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Added from web form.")
            return_value = super(AddApp, self).form_valid(form)
        return return_value


class UpdateApp(edit.UpdateView):
    template_name = 'app_form.html'
    model = models.App
    success_url = reverse_lazy('app_list')
    fields = ['name', 'repo_url', 'repo_type', 'buildpack', 'stack']
    slug_field = 'name'

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Updated from web form.")
            return_value = super(UpdateApp, self).form_valid(form)
        return return_value


class DeleteApp(edit.DeleteView):
    model = models.App
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('app_list')

    def delete(self, request, *args, **kwargs):
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Deleted from web form.")
            return super(DeleteApp, self).delete(request)


# Buildpack views
class ListBuildPack(ListView):
    model = models.BuildPack
    template_name = 'buildpack_list.html'


class AddBuildPack(edit.CreateView):
    template_name = 'buildpack_form.html'
    model = models.BuildPack
    success_url = reverse_lazy('buildpack_list')

    # Get rid of the following message:
    # Using ModelFormMixin (base class of AddBuildPack) without the 'fields'
    # attribute is prohibited.
    fields = ['repo_url', 'repo_type', 'desc', 'order']

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Added from web form.")
            return_value = super(AddBuildPack, self).form_valid(form)
        return return_value


class UpdateBuildPack(edit.UpdateView):
    template_name = 'buildpack_form.html'
    model = models.BuildPack
    success_url = reverse_lazy('buildpack_list')

    fields = ['repo_url', 'repo_type', 'desc', 'order']

    def form_valid(self, form):
        """
        Override so we can setup django-reversion versioning.
        """
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Updated from web form.")
            return_value = super(UpdateBuildPack, self).form_valid(form)
        return return_value


class DeleteBuildPack(edit.DeleteView):
    model = models.BuildPack
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('buildpack_list')

    def delete(self, request, *args, **kwargs):
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Deleted from web form.")
            return super(DeleteBuildPack, self).delete(request)


# Stack views
class ListStack(ListView):
    model = models.OSStack
    template_name = 'stack_list.html'


@login_required
def edit_stack(request, stack_id=None):
    if stack_id:
        stack = models.OSStack.objects.get(id=stack_id)
    else:
        stack = None

    form = forms.StackForm(request.POST or None, request.FILES or None,
                           instance=stack)

    if form.is_valid():
        form.save()
        stack = form.instance  # In case we just made a new one.

        if form.cleaned_data['build_now']:
            # Image names should look like stackname_date_counter
            name_prefix = '%s_%s_' % (
                form.instance.name,
                datetime.datetime.today().strftime('%Y%m%d'),
            )
            builds_today = models.OSImage.objects.filter(
                name__startswith=name_prefix).count()
            image_name = name_prefix + str(builds_today + 1)
            image = models.OSImage(
                stack=stack,
                name=image_name,
                base_image_url=form.instance.base_image_url,
                base_image_name=form.instance.name + '_base',
                provisioning_script_url=form.instance.provisioning_script.url,
            )
            image.save()
            events.eventify(
                request.user, 'build image', image,
                resource_uri='/stack/{}/'.format(image.id))
            tasks.build_image.delay(image.id)
        return redirect('dash')
    values = dict(
        form=form,
        object=stack,
        enctype='multipart/form-data',
    )
    return render(request, 'stack_form.html', values)


class DeleteStack(edit.DeleteView):
    model = models.OSStack
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('stack_list')

    def delete(self, request, *args, **kwargs):
        with create_revision():
            revisions.set_user(self.request.user)
            revisions.set_comment("Deleted from web form.")
            return super(DeleteStack, self).delete(request)


def login(request):
    form = forms.LoginForm(request.POST or None)
    if form.is_valid():
        # log the person in.
        django_login(request, form.user)
        # redirect to next or home
        return HttpResponseRedirect(request.GET.get('next', '/'))
    return render(request, 'login.html', {
        'form': form,
        'hide_nav': True
    })


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')
