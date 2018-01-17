import os, sys
from envparse import env
import ldap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '8vsbrlm2=53ag(&yye0bw#+qw^-^#azzw66&_!)3r(kzbi9$h-'

DEBUG = True

ALLOWED_HOSTS = ['asdd-dev.weber.edu', 'localhost', 'chitester.weber.edu']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',
    'jsoneditor',
    'api',
    'db',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'genisys.security.GenisysSecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'genisys.urls'

JSON_EDITOR_JS = 'jsoneditor/jsoneditor.js'
JSON_EDITOR_CSS = 'jsoneditor/jsoneditor.css'

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

WSGI_APPLICATION = 'genisys.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'genisyseval',
        'USER': 'evaldev',
        'PASSWORD': 'Bradp3750',
        'HOST': 'genisys.cz5n9hahvziy.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    },

}

DATABASE_ROUTERS = ['convert.routers.ConvertRouter',]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Mountain'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR+"/../", 'www', 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR+"/../", 'www', 'media')

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0,
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER,
    ldap.OPT_X_TLS_CRLCHECK: ldap.OPT_X_TLS_NEVER,
    ldap.OPT_X_TLS_NEWCTX: 0,
    ldap.OPT_SIZELIMIT: 2400
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend'
)

AUTH_USER_MODEL = 'db.User'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'genisys': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
