# pylint: disable=old-style-class,no-init,no-self-use
from __future__ import print_function

import contextlib
import json
import logging
import re

import six
from six.moves import configparser
from backports.functools_lru_cache import lru_cache

import path
import jaraco.context

from django.conf.urls import url
from django.http import (HttpResponse, HttpResponseNotAllowed,
                         HttpResponseNotFound)
from django.contrib.auth.models import User

import reversion as revisions
from reversion import create_revision

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie import authentication as auth
from tastypie.authorization import Authorization
from tastypie.api import Api
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.utils import trailing_slash

from vr.server import models
from vr.server.views import do_swarm, do_build, do_deploy
from vr.server.api.views import auth_required
from vr.server.utils import yamlize

logger = logging.getLogger('velociraptor.api')

# XXX Note that procs don't have a resource in this file.  It turns out that
# Tastypie is not as good at handling non-ORM resources as I was led to
# believe.  I made an effort, and ended up getting it mostly working, but it
# was ugly as hell and using tons of subclasses and overrides.  In the end I
# decided to just write a Django view and hard-code a route to
# /api/v1/hosts/<name>/procs/. --Brent

v1 = Api(api_name='v1')


def register_instance(cls):
    v1.register(cls())
    return cls


@contextlib.contextmanager
def revision_ctx(bundle, comment):
    with create_revision():
        try:
            # We are not sure if request.user is in bundle all the times
            revisions.set_user(bundle.request.user)
        except Exception:
            logger.exception('Cannot set user in revision')
        revisions.set_comment(comment)
        yield


class ReversionModelResource(ModelResource):
    """ Add django-reversion calls to methods that write to the db.
    """
    def obj_create(self, bundle, **kwargs):
        with revision_ctx(bundle, 'Created from the API.'):
            return super(
                ReversionModelResource, self).obj_create(bundle, **kwargs)

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        with revision_ctx(bundle, 'Updated from the API.'):
            return super(
                ReversionModelResource, self).obj_update(
                    bundle, skip_errors, **kwargs)

    def obj_delete_list(self, bundle, **kwargs):
        with revision_ctx(bundle, 'Deleted list from the API.'):
            return super(
                ReversionModelResource, self).obj_delete_list(bundle, **kwargs)

    def obj_delete_list_for_update(self, bundle, **kwargs):
        with revision_ctx(bundle, 'Deleted list for update from the API.'):
            return super(
                ReversionModelResource, self).obj_delete_list_for_update(
                    bundle, **kwargs)

    def obj_delete(self, bundle, **kwargs):
        with revision_ctx(bundle, 'Deleted from the API.'):
            return super(
                ReversionModelResource, self).obj_delete(bundle, **kwargs)


@register_instance
class SquadResource(ReversionModelResource):
    hosts = fields.ToManyField('vr.server.api.resources.HostResource', 'hosts',
                               full=True)

    class Meta:
        queryset = models.Squad.objects.all()
        resource_name = 'squads'
        filtering = {
            'hosts': ALL_WITH_RELATIONS,
        }
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()
        detail_uri_name = 'name'


@register_instance
class IngredientResource(ReversionModelResource):
    swarms = fields.ToManyField(
        'vr.server.api.resources.SwarmResource', 'swarm_set',
        blank=True, null=True, readonly=True)

    class Meta:
        queryset = models.ConfigIngredient.objects.all()
        filtering = {
            'name': ALL,
        }
        resource_name = 'ingredients'
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()


@register_instance
class AppResource(ReversionModelResource):
    buildpack = fields.ToOneField(
        'vr.server.api.resources.BuildPackResource',
        'buildpack', null=True)
    stack = fields.ToOneField(
        'vr.server.api.resources.StackResource',
        'stack', null=True)

    class Meta:
        queryset = models.App.objects.select_related(
            'buildpack', 'stack').all()
        resource_name = 'apps'
        filtering = {
            'id': ALL,
            'name': ALL,
            'buildpack': ALL_WITH_RELATIONS,
            'stack': ALL_WITH_RELATIONS,
        }
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()
        detail_uri_name = 'name'

    def dehydrate(self, bundle):
        canon_url = self.resolve_url(bundle.data['repo_url'])
        bundle.data['resolved_url'] = canon_url or bundle.data['repo_url']
        return bundle

    @classmethod
    def resolve_url(cls, spec_url):
        """
        Expand schemes in the URL based on schemes defined
        Mercurial-style.
        """
        mapping = cls.load_schemes() or {}

        def replace(match):
            return mapping.get(match.group('scheme'), match.group(0))
        return re.sub(r'^(?P<scheme>\w+)://', replace, spec_url)

    @staticmethod
    @lru_cache()
    @jaraco.context.suppress(Exception)
    def load_schemes():
        """
        Read schemes from a config file expecting the format:

        [schemes]
        scheme = https://example.com/

        Roughly compatible with Mercurial's schemes definitions.

        Failsafe - never raises an exception, but returns None
        """
        parser = configparser.ConfigParser()
        parser.read(path.Path('~/.hgrc').expanduser())
        return dict(parser.items('schemes')) if six.PY2 else parser['schemes']


@register_instance
class BuildPackResource(ReversionModelResource):
    class Meta:
        queryset = models.BuildPack.objects.all()
        resource_name = 'buildpacks'
        filtering = {
            'repo_url': ALL,
            'repo_type': ALL,
        }
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()


@register_instance
class StackResource(ReversionModelResource):
    class Meta:
        queryset = models.OSStack.objects.all()
        resource_name = 'stacks'
        filtering = {
            'id': ALL,
            'name': ALL,
        }
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()
        detail_uri_name = 'name'


@register_instance
class BuildResource(ReversionModelResource):
    app = fields.ToOneField('vr.server.api.resources.AppResource', 'app')

    class Meta:
        queryset = models.Build.objects.select_related('app').all()
        resource_name = 'builds'
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()
        filtering = {
            'app': ALL_WITH_RELATIONS,
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/build%s$" %
                (self._meta.resource_name, trailing_slash()),
                auth_required(
                    self.wrap_view('do_build')),
                name="api_do_build"),
        ]

    def do_build(self, request, **kwargs):

        if request.method != 'POST':
            return HttpResponseNotAllowed(["POST"])

        try:
            build = models.Build.objects.get(id=int(kwargs['pk']))
            # Set the build OS image, from the coresponding app.
            build.os_image = build.app.get_os_image()
            # Need to save it, so async tasks will find the new OS image
            build.save()
        except models.Build.DoesNotExist:
            return HttpResponseNotFound()

        do_build(build, request.user)

        # Status 202 means "The request has been accepted for processing, but
        # the processing has not been completed."
        return HttpResponse(status=202)


@register_instance
class SwarmResource(ReversionModelResource):
    app = fields.ToOneField('vr.server.api.resources.AppResource', 'app')
    squad = fields.ToOneField('vr.server.api.resources.SquadResource', 'squad')

    # Leave 'release' blank when you want to set 'version' to
    # something new, and the model will intelligently create a new
    # release for you.
    release = fields.ToOneField(
        'vr.server.api.resources.ReleaseResource', 'release',
        blank=True, null=True)

    shortname = fields.CharField('shortname')
    volumes = fields.ListField('volumes', null=True)
    config_ingredients = fields.ToManyField(
        'vr.server.api.resources.IngredientResource',
        'config_ingredients')
    compiled_config = fields.DictField('get_config')
    compiled_env = fields.DictField('get_env')
    version = fields.CharField('version')

    class Meta:
        queryset = models.Swarm.objects.select_related(
            'app', 'squad', 'release'
        ).prefetch_related(
            'config_ingredients', 'squad__hosts',
            'release__build', 'release__build__app',
        ).all()
        resource_name = 'swarms'
        filtering = {
            'ingredients': ALL_WITH_RELATIONS,
            'squad': ALL_WITH_RELATIONS,
            'app': ALL_WITH_RELATIONS,
            'proc_name': ALL,
            'config_name': ALL,
            'pool': ALL,

        }
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()

    def dehydrate(self, bundle):
        # add in proc data
        # TODO: Make these proper attributes so they can be saved by a
        # PUT/POST to the swarm resource.
        bundle.data['procs_uri'] = bundle.data['resource_uri'] + 'procs/'
        bundle.data['procs'] = [p.as_dict() for p in
                                bundle.obj.get_procs(check_cache=True)]
        bundle.data['squad_name'] = bundle.obj.squad.name

        # Also add in convenience data
        bundle.data.update(app_name=bundle.obj.app.name,
                           config_name=bundle.obj.config_name)
        return bundle

    def dehydrate_env_yaml(self, bundle):
        # Explicit dehydrate to avoid this field is stringified with str()
        return yamlize(bundle.obj.env_yaml)

    def dehydrate_config_yaml(self, bundle):
        # Explicit dehydrate to avoid this field is stringified with str()
        return yamlize(bundle.obj.config_yaml)

    def hydrate(self, bundle):
        # delete the compiled_config and compiled_env keys in the
        # bundle, because they can cause hydration problems if
        # tastypie tries to set them.
        bundle.data.pop('compiled_config', None)
        bundle.data.pop('compiled_env', None)

        # If version is provided, that takes priority over release
        if 'version' in bundle.data:
            bundle.data.pop('release', None)
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/swarm%s$" %
                (self._meta.resource_name, trailing_slash()),
                auth_required(
                    self.wrap_view('do_swarm')),
                name="api_do_swarm"),
        ]

    def do_swarm(self, request, **kwargs):

        if request.method == 'POST':
            try:
                swarm = models.Swarm.objects.get(id=int(kwargs['pk']))
            except models.Swarm.DoesNotExist:
                return HttpResponseNotFound()

            swarm_id = do_swarm(swarm, request.user)

            # Status 202 means "The request has been accepted for
            # processing, but the processing has not been completed."
            return HttpResponse(json.dumps({'swarm_id': swarm_id}),
                                status=202,
                                content_type='application/json')

        return HttpResponseNotAllowed(["POST"])

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(SwarmResource, self).apply_filters(
            request, applicable_filters
        )

        # Allow filtering Swarms on pool name, like so:
        # /api/v1/swarms/?pool=[pool_name]
        pool = request.GET.get('pool', None)
        if pool:
            base_object_list = base_object_list.filter(pool=pool)

        return base_object_list


@register_instance
class ReleaseResource(ReversionModelResource):
    build = fields.ToOneField('vr.server.api.resources.BuildResource', 'build')
    compiled_name = fields.CharField('get_name')

    class Meta:
        queryset = models.Release.objects.select_related('build').all()
        resource_name = 'releases'
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()
        filtering = {
            'build': ALL_WITH_RELATIONS,
        }

    def prepend_urls(self):
        pattern = (
            r'^(?P<resource_name>{meta.resource_name})'
            r'/(?P<pk>\w[\w/-]*)/deploy{trailing_slash}$'
        ).format(meta=self._meta, trailing_slash=trailing_slash())
        return [
            url(
                pattern,
                auth_required(self.wrap_view('deploy_release')),
                name="api_deploy_release",
            ),
        ]

    def deploy_release(self, request, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed(["POST"])

        try:
            release = models.Release.objects.get(id=int(kwargs['pk']))
        except models.Swarm.DoesNotExist:
            return HttpResponseNotFound()

        data = json.loads(request.body)
        do_deploy(release, request.user, data['config_name'], data['host'],
                  data['proc'], data['port'])

        # Status 202 means "The request has been accepted for processing, but
        # the processing has not been completed."
        return HttpResponse(status=202)


@register_instance
class TestResultResource(ModelResource):
    testrun = fields.ToOneField(
        'vr.server.api.resources.TestRunResource', 'run',
        related_name='tests')

    class Meta:
        queryset = models.TestResult.objects.all()
        resource_name = 'testresults'
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()


@register_instance
class TestRunResource(ModelResource):
    testresults = fields.ToManyField(
        'vr.server.api.resources.TestResultResource',
        'tests', full=True)

    class Meta:
        queryset = models.TestRun.objects.all()
        resource_name = 'testruns'
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()


@register_instance
class HostResource(ReversionModelResource):
    squad = fields.ToOneField('vr.server.api.resources.SquadResource', 'squad',
                              null=True, blank=True)

    class Meta:
        queryset = models.Host.objects.select_related('squad').all()
        resource_name = 'hosts'
        filtering = {
            'name': ALL,
            'active': ALL,
        }
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()
        detail_uri_name = 'name'

    def dehydrate(self, bundle):
        bundle.data['procs_uri'] = bundle.data['resource_uri'] + 'procs/'
        bundle.data['procs'] = [p.as_dict() for p in
                                bundle.obj.get_procs(check_cache=True)]
        return bundle


@register_instance
class LogResource(ModelResource):
    user = fields.ToOneField(
        'vr.server.api.resources.UserResource', 'user', full=True)

    class Meta:
        queryset = models.DeploymentLogEntry.objects.all()
        resource_name = 'logs'
        filtering = {
            'type': ALL,
            'time': ALL,
            'user': ALL_WITH_RELATIONS,
            'message': ALL,
        }
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()


@register_instance
class UserResource(ModelResource):
    profile = fields.ToOneField(
        'vr.server.api.resources.ProfileResource', 'userprofile',
        full=True, null=True,
        blank=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = [
            'email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }
        authentication = auth.MultiAuthentication(
            auth.BasicAuthentication(),
            auth.SessionAuthentication(),
        )
        authorization = Authorization()


@register_instance
class ProfileResource(ModelResource):
    default_dashboard = fields.ToOneField(
        'vr.server.api.resources.DashboardResource', 'default_dashboard',
        null=True, blank=True)
    quick_dashboards = fields.ToManyField(
        'vr.server.api.resources.DashboardResource', 'quick_dashboards',
        null=True, blank=True)

    class Meta:
        queryset = models.UserProfile.objects.all()
        resource_name = 'profile'
        authorization = Authorization()


@register_instance
class DashboardResource(ReversionModelResource):
    apps = fields.ToManyField(
        'vr.server.api.resources.AppResource', 'apps',
        null=True, blank=True, full=True)

    class Meta:
        queryset = models.Dashboard.objects.all()
        resource_name = 'dashboard'
        authorization = Authorization()
