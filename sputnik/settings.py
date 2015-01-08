"""
Django settings for sputnik project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'INSERT_SECRET_KEY_HERE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Required by allauth
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'rest_framework',

    'haystack',

    'widget_tweaks',

    'pipeline',

    'sputnik',
    'users',
    'podcasts',
    'news',

    # 'debug_toolbar',
)

INTERNAL_IPS = '0.0.0.0', '127.0.0.1'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
)

ROOT_URLCONF = 'sputnik.urls'

WSGI_APPLICATION = 'sputnik.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    # Required by allauth template tags
    "django.core.context_processors.request",

    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_CONFIRM_EMAIL_ON_GET = True

ACCOUNT_EMAIL_SUBJECT_PREFIX = "PodFlare - "

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Pipeline settings
#STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
#PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'
#PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.csstidy.CSSTidyCompressor'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': 'mypguser',
        'PASSWORD': 'pass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Required to have this setting by allauth
SITE_ID = 1


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'sputnik/static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'podcasts/templates'),
    os.path.join(BASE_DIR, 'news/templates'),
    os.path.join(BASE_DIR, 'users/templates'),
    os.path.join(BASE_DIR, 'sputnik/templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
