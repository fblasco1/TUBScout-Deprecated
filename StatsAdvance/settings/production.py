from .base import *
import django_heroku

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd8n8462eetj13u',
        'USER': 'lxhyphrjgeyvvn',
        'PASSWORD': 'adcac99021773ffb2c82362569f9ead7edff7b1e6e681a60e3db20faf60cb895',
        'HOST': 'ec2-34-234-228-127.compute-1.amazonaws.com',
        'PORT': '5432',
        }
}

STATICFILES_DIRS = (BASE_DIR,'static')

django_heroku.settings(locals())