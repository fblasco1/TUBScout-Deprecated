from .base import *
import django_heroku

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DEBUG = False

ALLOWED_HOSTS = ['tubscout.herokuapp.com']

DATABASES = {
'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd9pjc95l9k9mjt',
        'USER': 'yapsamtcvfjeco',
        'PASSWORD': '27e0ee76c25d6ccb0185a4008ce27cbfbfb44745eaa1825859c05bf6d72093fa',
        'HOST': 'ec2-34-234-228-127.compute-1.amazonaws.com',
        'PORT': '5432',
        }
}

STATICFILES_DIRS = (BASE_DIR,'static')

django_heroku.settings(locals())