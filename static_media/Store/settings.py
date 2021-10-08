import os
from pathlib import Path
from django.contrib.messages import constants as messages
from decouple import DEFAULT_ENCODING, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'd*66=tumtt@k+xi^lp7+l4^mh^^u4p^-tdk#tll-vveq4xq+rl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.apps.AppConfig',
    'accounts.apps.AccountsConfig',
    'products.apps.ProductsConfig',
    'orders.apps.OrdersConfig',
    'cart.apps.CartConfig',
    'froala_editor',
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'corsheaders',

]
# 'storages',

# only if django version >= 3.0
X_FRAME_OPTIONS = 'SAMEORIGIN'
SILENCED_SYSTEM_CHECKS = ['security.W019']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'Store.urls'
CORS_ORIGIN_ALLOW_ALL = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processor.menu_links',
                'cart.context_processor.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'Store.wsgi.application'
AUTH_USER_MODEL = 'accounts.Account'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'storeDB',
            'USER': 'postgres',
            'PASSWORD': 'parkash0008@',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Canada/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_media'

STATICFILES_DIRS = [
    BASE_DIR, "static",
]


# # AWS S3 Static Files Configuration
# AWS_ACCESS_KEY_ID = 'AKIAQGXP3I4TFGK7OG5F'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = 'store-s3-bucket'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = 'public-read'
# AWS_LOCATION = 'static'

# STATICFILES_DIRS = [
#     BASE_DIR/"static",
# ]
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# media root

MEDIA_ROOT = BASE_DIR, 'media'

MEDIA_URL = '/media/'

MESSAGE_TAGS = {
    messages.INFO: 'danger',
    messages.SUCCESS: 'success',
}

# DEFAULT_FILE_STORAGE = "Store.media_storages.MediaStorage"

# Email Sending
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_PORT = config('EMAIL_PORT', cast=int)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_BACKEND = config('EMAIL_BACKEND')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'humpty.dumpty.ontario.inc@gmail.com'
EMAIL_HOST_PASSWORD = 'parkash0008@'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
