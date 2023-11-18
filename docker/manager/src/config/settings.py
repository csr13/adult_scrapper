import os
import importlib

from pathlib import Path


def bool_env(env):
    return True if env == 'true' else False


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-fw0v^)3b3#!z-w@=rfe7(xs$_&7yv3&e=^b90c=%)-3##kel5$'
)

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'manager'
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "manager" / "templates"
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER' : os.getenv("DB_USER"),
        'PASSWORD' : os.getenv("DB_PASSWORD"),
        'HOST' : 'database',
        'POST' : 5432
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIR = [
    BASE_DIR / "manager" / "static"
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

#################################
# FEED
#################################

FEED_URL = "http://feed:8888"

#################################
# XXX_SITE
#################################

# Fallback to local development of porn site
XXX_SITE_URL = os.getenv("XXX_SITE_URL", "http://172.19.0.2:8000")

XXX_SITE_ADMIN_API_KEY = os.getenv("XXX_SITE_ADMIN_API_KEY")

#################################
# API CONFIG
#################################

API_AUTH = bool_env(os.getenv('API_AUTH', 'false'))

JSON_WEB_TOKEN_AUTH = bool_env(os.getenv('JSON_WEB_TOKEN_AUTH', 'false'))

PERMISSION_CLASSES = []

AUTHENTICATION_CLASSES = []

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}

if JSON_WEB_TOKEN_AUTH:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append(
        'rest_framework_simplejwt.authentication.JWTAuthentication' 
    )

if API_AUTH:
    from rest_framework.authentication import SessionAuthentication
    from rest_framework.permissions import IsAuthenticated
    PERMISSION_CLASSES.append(IsAuthenticated)
    AUTHENTICATION_CLASSES.append(SessionAuthentication)

ALLOWED_INTERNAL_ACCESS_ADDRESSES = [
    "172.18.0.2", # feed
]
