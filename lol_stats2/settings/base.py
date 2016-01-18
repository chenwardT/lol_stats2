"""
Django settings for lol_stats2 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.core.exceptions import ImproperlyConfigured
from kombu import Queue

from .secrets import DJANGO_SECRET_KEY, PG_USER, PG_PASS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = DJANGO_SECRET_KEY

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'summoners',
    'champions',
    # 'games',
    'spells',
    'leagues',
    'matches',
    'stats',
]

RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8001'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}

CELERYD_POOL_RESTARTS = True

# TODO: Refine MQ topology.
CELERY_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('match_ids', routing_key='match_ids'),
    Queue('store', routing_key='store.#'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'

# TODO: Consolidate routing rules.
CELERY_ROUTES = {
    'lol_stats2.celery.store_match': {
        'queue': 'store',
        'exchange': 'default',
        'exchange_type': 'topic',
        'routing_key': 'store.get_match',
    },
    'riot_api.wrapper.get_matches_from_ids': {
        'queue': 'match_ids',
        'exchange': 'default',
        'exchange_type': 'topic',
        'routing_key': 'match_ids',
    }
}

# This should be set in test virtualenv.
# Causes all tasks to be executed locally by blocking until task returns.
if 'CELERY_ALWAYS_EAGER' in os.environ:
    CELERY_ALWAYS_EAGER = True

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
]

ROOT_URLCONF = 'lol_stats2.urls'

WSGI_APPLICATION = 'lol_stats2.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s,%(msecs)03d] %(levelname)s [%(name)s:%(lineno)s] %(funcName)s: %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log/debug.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'cache': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        'champions': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        'games': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        'leagues': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        # Some celery tasks are defined here, see celery.py
        'lol_stats2': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'matches': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        'riot_api': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        'spells': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        'summoners': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        'utils': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        # python shell
        'shell': {
            'handlers': ['file'],
            'level': 'DEBUG'
        }

    }
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'NAME': 'lol_stats2',
        'USER': PG_USER,
        'PASSWORD': PG_PASS,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TODO: Consider TZ agnostic and assume GMT.
# DateTimeFields on models store timezone offset!
# ex. 2015-05-11 20:42:10.712697-04
TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'