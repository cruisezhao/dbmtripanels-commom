"""the base settings is shared with another project"""


import os
import datetime
from django.core.urlresolvers import reverse_lazy
import socket

hostname = socket.gethostname()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'authtools',
    'crispy_forms',

    'common.apps.accounts',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        # Or path to database file if using sqlite3.
        'NAME': 'cluster',
        'USER': 'cluster',                      # Not used with sqlite3.
        'PASSWORD': 'Data8ase-cluster',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '45.35.50.34',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '3306',
        #'OPTIONS': {'init_command': 'SET storage_engine=INNODB;'}
    },
}

#Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ADMINS = [('taylor', 'taylor.h.dbm@gmail.com'),('huangqi','806749175@qq.com')]

EMAIL_HOST = 'mail.jucuyun.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'Taylor@jucuyun.com'
EMAIL_HOST_PASSWORD = 'TPUOErSQE8cJ'
DEFAULT_FROM_EMAIL = 'Taylor@jucuyun.com'
EMAIL_SUBJECT_PREFIX = '[jucuyun]'
#admin mail
SERVER_EMAIL = 'Taylor@jucuyun.com'


# Authentication Settings
AUTH_USER_MODEL = 'clients.Clients'
LOGIN_REDIRECT_URL = reverse_lazy("home")
LOGIN_URL = reverse_lazy("accounts:login")

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT =os.path.join(BASE_DIR,'static')

CORS_ORIGIN_ALLOW_ALL=True

#jwt settings
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60*60*24),
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

    # Cookie name. This can be whatever you want.
TOKEN_COOKIE_NAME = 'token'
# Age of cookie, in seconds (default: 2 weeks).
TOKEN_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# A string like ".example.com", or None for standard domain cookie.
# If you test in domain 127.0.0.1, then you must comment out the databasemart.net, and use empty value
if hostname == 'cluster':
    TOKEN_COOKIE_DOMAIN = '.tripanels.com'
else:
    TOKEN_COOKIE_DOMAIN = ''
# Whether the session cookie should be secure (https:// only).
TOKEN_COOKIE_SECURE = False
# The path of the session cookie.
TOKEN_COOKIE_PATH = '/'
# Whether to use the non-RFC standard httpOnly flag (IE, FF3+, others)
TOKEN_COOKIE_HTTPONLY = False
