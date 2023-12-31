"""
Django settings for server_balance project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_NAME = "server_balance"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8!1b=&61!s6+_uhkg==#df1)=*^-(6sw!at6fso)z3cg-ljc_7'

# encrypt sms otp
FERNET_KEY = b'0siKzDBkux4VEDGEcIPHnJLH7YKDMJr_Pn9R93fA3Lk='
RECHARGE_KEY = "a6378f-608559-21f1ae-d86915-8fcb43"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*", "192.168.137.1"]

#ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.1.1", "192.168.1.8", "192.168.134.39", "192.168.137.1", "192.168.137.89", "192.168.137.63", "oven.com", "*"]
#python manage.py runserver 0.0.0.0:8000
#pip freeze > requirements.txt

# Step1 : python manage.py collectstatic


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'rest_framework',
    'welcome',       # welcome for login, Registration
    # 'device',        # have models + Api's
    'myconst',       # only constants models

    # 'user_guest',    #G  
    # 'user_operator', #O
    # 'user_admin',    #A customers Authority

    # 'user_staff',    #S Company Authority
    # 'user_master',   #M Company Admin

    'import_export',
    # 'debug_toolbar',
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server_balance.urls'

# REST_FRAMEWORK = { 
#     'DEFAULT_AUTHENTICATION_CLASSES': ( 
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#         #'rest_framework.renderers.BrowsableAPIRenderer',
#     ]
# }
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': False,
#     'UPDATE_LAST_LOGIN': False,

#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': SECRET_KEY,
#     'VERIFYING_KEY': None,
#     'AUDIENCE': None,
#     'ISSUER': None,
#     'JWK_URL': None,
#     'LEEWAY': 0,

#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
#     'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     'TOKEN_TYPE_CLAIM': 'token_type',
#     'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

#     'JTI_CLAIM': 'jti',

#     'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
#     'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
# }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'server_balance.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#For new setup db, only delete _pycache_ and migrations file (not delete __init__.py file inside of migrations)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'DBname',
#         'USER': "DBuser",
#         'PASSWORD': 'DBpassword',
#         'HOST': 'dbname.cso39ocu5qbi.ap-south-1.rds.amazonaws.com',
#         'PORT': '5432'
#     }
# }

# (github key) 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

# ================== from redis ======================
# CACHE_TTL = 2 * 60 * 60   # 2hours

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         },
#         "KEY_PREFIX": "example"
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC' 
TIME_ZONE =  'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if DEBUG:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, PROJECT_NAME + '/static')
    STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static')]
    # MEDIAFILES_DIRS = [ BASE_DIR / "media", ]
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
else: 
    STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static')]
    STATIC_ROOT = os.path.join(BASE_DIR / 'static')
    STATIC_URL = '/static/'
    MEDIA_ROOT = os.path.join(BASE_DIR / 'media')
    MEDIA_URL = '/media/'



'''CRONJOBS = [
    ('*/1 * * * *', 'welcome.cron.my_scheduled_job')
]'''

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 4*60*60
CSRF_COOKIE_AGE = 4*60*60
#SESSION_SAVE_EVERY_REQUEST = True

#bootstrap message
try:
    from django.contrib.messages import constants as messages
    MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
    }
except Exception as e:
    pass

# django import export
IMPORT_EXPORT_CHUNK_SIZE = 1000

# for tool debuger
INTERNAL_IPS = [
    '127.0.0.1',
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
