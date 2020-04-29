from .base import *
import dj_database_url
import django_heroku

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DEBUG = True

ALLOWED_HOSTS = ['tubscout.herokuapp.com']

DATABASES = {
'default': { }
}

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

STATICFILES_DIRS = (BASE_DIR,'static')

django_heroku.settings(locals())