"""
This module is designed to be used by this app. The purpose of this module is
to provide default values for the settings, and to implement a hook so other
modules in the app need only import this settings module, rather than the
Django project settings as well.

This module also provides settings needed to run this app without the need for
a larger project context.

Generated by 'django-admin startproject' using Django 2.0.4.
"""

try:
    from django.conf import settings
except ImportError:
    class settings: pass
import os
import sys


def get_setting(name):
    """
    Hook for getting Django settings without modules having to import it.
    Project settings dominate, otherwise use the default here.
    """
    me = sys.modules[__name__]
    return getattr(settings, name, getattr(me, name, None))


# setting `base_dir` before defaults since it needs to be used by `DATABASES`.
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# This section defines settings required for the app to run standalone.
BASE_DIR = base_dir
SECRET_KEY = 'not-a-very-good-secret'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django_purge',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'django_purge.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'django_purge.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(base_dir, 'db.sqlite3'),
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
APPEND_SLASH = True

CRON_CLASSES = [
    'django_purge.cron.CronJob',
]
