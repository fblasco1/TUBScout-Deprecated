from .base import *

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'statsadvancedb',
        'USER': 'postgres',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': '5432',
        }
}

STATICFILES_DIRS = (BASE_DIR,'static')