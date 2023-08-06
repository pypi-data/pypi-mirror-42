import sys
import importlib

import os
import logging
import datetime
import socket

import pkg_resources
import djcelery
from celery.schedules import crontab
import pymongo

if 'runserver' in sys.argv:
    from gevent import monkey
    monkey.patch_all()
    importlib.import_module('psycogreen.gevent').patch_psycopg()

here = os.path.dirname(os.path.realpath(__file__))
parentpath = os.path.dirname(here)

DEBUG = True
TEMPLATE_DEBUG = DEBUG
if not DEBUG:
    ALLOWED_HOSTS = ['*']

ADMINS = ()

MANAGERS = ADMINS
SERVER_EMAIL = 'velociraptor@' + socket.getfqdn()
CELERY_SEND_TASK_ERROR_EMAILS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'velo',
        'USER': 'raptor',
        'PASSWORD': 'MZpuvFzZ',
        'HOST': 'localhost',
        'PORT': '',
    }
}

BALANCERS = {
    'default': {
        'BACKEND': 'vr.server.balancer.dummy.DummyBalancer',
    }
}

# Without this, the build host will choke when trying to connect to a local
# redis that doesn't exist.
if 'collectstatic' not in sys.argv and not os.getenv('COLLECTSTATIC'):
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': 'localhost:6379',
            'KEY_PREFIX': 'vrcache_',
            'OPTIONS': {
                'DB': 0,
            },
        },
    }

# UI Customization.  It's good to make your non-production instances look
# different from production.
SITE_TITLE = "Velociraptor"
# URL to a custom CSS file
CUSTOM_CSS = None

USE_TZ = True

# Username and password to be used when SSHing to hosts.  Set to
# 'vagrant/vagrant' by default for ease of development within a Vagrant VM.
DEPLOY_USER = 'vagrant'
DEPLOY_PASSWORD = 'vagrant'

MONGODB_URL = 'mongodb://localhost/velociraptor'

CELERY_ENABLE_UTC = True
CELERYBEAT_SCHEDULER = 'celery_schedulers.redis_scheduler.RedisScheduler'
CELERYBEAT_SCHEDULE_FILENAME = 'redis://localhost:6379/0'
CELERYD_CONCURRENCY = 4

# Time limits
CELERYD_TASK_TIME_LIMIT = 3600

# Use Redis broker and results backend by default.  The RabbitMQ one isn't as
# nice for chords.
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# URL for the redis instance where all pubsub notices will be pushed.
EVENTS_PUBSUB_URL = 'redis://localhost:6379/0'

# Deployment event messages are put on this channel by the worker procs
EVENTS_PUBSUB_CHANNEL = 'vr2_events'

# The most recent deployment events are cached so the dashboard can show what
# has happened lately.
EVENTS_BUFFER_KEY = 'vr2_events_buffer'
EVENTS_BUFFER_LENGTH = 100

# Event listener plugins on the application-running hosts should be configured
# to send proc status messages to this channel on the redis at
# EVENTS_PUBSUB_URL.
PROC_EVENTS_CHANNEL = 'proc_events'

CELERYBEAT_SCHEDULE = {
    'filesystem_scooper': {
        'task': 'vr.server.tasks.filesystem_scooper',
        'schedule': crontab(hour='*/4', minute=5),
        'options': {
            'expires': 120,
        },
    },
    'procs_scooper': {
        'task': 'vr.server.tasks.procs_scooper',
        'schedule': crontab(minute='*/30'),
        'options': {
            'expires': 120,
        },
    },
    'test_all_the_things': {
        'task': 'vr.server.tasks.uptest_all_procs',
        'schedule': datetime.timedelta(minutes=60),
        'options': {
            'expires': 120,
        },
    },
    'clean_old_builds': {
        'task': 'vr.server.tasks.clean_old_builds',
        'schedule': crontab(hour=12, minute=15),
        'options': {
            'expires': 120,
        },
    },
}

CELERY_ROUTES = {
    'vr.server.tasks.uptest_all_procs': {'queue': 'scheduled_uptests'},
    'vr.server.tasks.post_uptest_all_procs': {'queue': 'scheduled_uptests'},
    'vr.server.tasks.uptest_host': {'queue': 'scheduled_uptests'}
}

SUPERVISOR_PORT = 9001
SUPERVISOR_USERNAME = 'vagrant'
SUPERVISOR_PASSWORD = 'vagrant'
PORT_RANGE_START = 5000
PORT_RANGE_END = 6000

# Settings used when writing the proc.conf includes for supervisord
PROC_USER = 'nobody'
PROC_SYSLOG = False

# Local time zone for this installation.  On Unix systems, a value of None will
# cause Django to use the same timezone as the operating system.
TIME_ZONE = None

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False
USE_L10N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"  NOTE that we don't actually
# use this in Velociraptor, because the default storage class is GridFS (Mongo)
MEDIA_ROOT = os.path.join(here, 'uploads/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/files/'

# Store files using mongodb gridfs by default.
DEFAULT_FILE_STORAGE = 'vr.server.storages.GridFSStorage'
STATICFILES_STORAGE = (
    'django.contrib.staticfiles.storage.CachedStaticFilesStorage')

# Use package's static folder if found, else fall back to local
STATIC_ROOT = pkg_resources.resource_filename('vr.server', 'static')

STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 't$fdltm55xt!a+chs_p-h9^7=-kh7@z$7salven903a%7v6c-i'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(here, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'vr.server.context_processors.raptor',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
LOGIN_URL = '/login/'

ROOT_URLCONF = 'vr.server.urls'

TEMPLATE_DIRS = (
    os.path.join(here, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'djcelery',
    'django_extensions',
    'vr.server',   # Velociraptor UI
    'reversion',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

SUPERVISORD_WEB_PORT = 9001

# If BUILD_EXPIRATION_DAYS is set to an integer instead of None, then the
# celerybeat proc will run a task every day to clean up old builds.  Regardless
# of the date cutoff, builds that are currently in use will be kept around, as
# well as the N most recent builds up to BUILD_EXPIRATION_COUNT.
BUILD_EXPIRATION_DAYS = 30
BUILD_EXPIRATION_COUNT = 10

API_LIMIT_PER_PAGE = 100

# Allow production to override these settings.
if os.environ.get('APP_SETTINGS_YAML'):
    import yaml
    try:
        app_settings = yaml.safe_load(
            open(os.environ['APP_SETTINGS_YAML'])) or {}
        globals().update(app_settings)
    except IOError:
        # Allow settings to be imported during build so we can compilestatic
        pass


# Unpack the MONGODB_URL env var to provide the settings that the GridFS
# storage wants.
mongoparts = pymongo.uri_parser.parse_uri(MONGODB_URL)
GRIDFS_HOST = mongoparts['nodelist'][0][0]
GRIDFS_PORT = mongoparts['nodelist'][0][1]
GRIDFS_DB = mongoparts['database'] or 'test'
GRIDFS_COLLECTION = mongoparts['collection'] or 'fs'

djcelery.setup_loader()


def setup_logger():
    """
    creates a logger named 'velociraptor'
    """
    logger = logging.getLogger('velociraptor')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    # create formatter
    template = '%(levelname)s [%(name)s] %(message)s'
    formatter = logging.Formatter(template)
    # add formatter to handler
    handler.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(handler)


setup_logger()


def setup_mailer():
    import celery.utils.mail

    # Remove exc stack trace from email subjects: it's already in the
    # email body
    celery.utils.mail.ErrorMail.subject = (
        '        [{hostname}] Error: Task {name} ({id})\n    '
    )


setup_mailer()


def setup_newrelic():
    # NewRelic is an optional dependency: don't fail if missing
    try:
        import newrelic.agent
    except ImportError:
        return

    # NewRelic initialisation uses environmental variables.
    # See https://docs.newrelic.com/docs/agents/python-agent
    #    /installation-configuration/python-agent-configuration

    # Typical usage:
    # - create a newrelic.ini file
    # - set env var NEW_RELIC_CONFIG_FILE to point to it
    # - optionally, specify an environment with NEW_RELIC_ENVIRONMENT
    newrelic.agent.initialize()


setup_newrelic()
