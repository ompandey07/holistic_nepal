#-- IMPORTS ---
from pathlib import Path
import os

#-- BASE DIRECTORY ---
BASE_DIR = Path(__file__).resolve().parent.parent

#-- SECURITY KEY ---
SECRET_KEY = 'django-insecure-lbpvaw*ke$&-r=1bahcn4)uc&^jmymod+6)$is%r&_i6scbeyz'

#-- DEBUG MODE ---
DEBUG = True

#-- ALLOWED HOSTS ---
ALLOWED_HOSTS = ['*']

#-- INSTALLED APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #-- LOCAL APPS ---
    'users',
    'core',
    'security',
    'admin_panel',
]

#-- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#-- ROOT URL CONFIG ---
ROOT_URLCONF = 'holistic_nepal.urls'

#-- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'Frontend'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.cart_context',
            ],
        },
    },
]

#-- WSGI APPLICATION ---
WSGI_APPLICATION = 'holistic_nepal.wsgi.application'

#-- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#-- PASSWORD VALIDATION ---
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

#-- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True

#-- DEFAULT AUTO FIELD ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'





#-- CACHE BACKEND ---
#-- USING LOCMEMCACHE (IN-PROCESS, ZERO-DEPENDENCY) FOR DASHBOARD AGGREGATION CACHING.
#-- TO SCALE TO MULTI-PROCESS OR MULTI-SERVER, SWAP BACKEND TO REDIS:
#--   'django.core.cache.backends.redis.RedisCache' WITH LOCATION='redis://127.0.0.1:6379/1'
CACHES = {
    'default': {
        'BACKEND':  'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'holistic-nepal-cache',
    }
}

#-- STATIC FILES SETTINGS (LOCAL + PRODUCTION) ---
STATIC_URL = '/static/'

#-- Folder(s) where Django looks for static files during development ---
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

#-- Folder where 'collectstatic' will gather all static files for production ---
STATIC_ROOT = BASE_DIR / 'staticfiles'

#-- MEDIA FILES SETTINGS (LOCAL + PRODUCTION) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'