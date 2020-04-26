from .base import *
from decouple import config
import dj_database_url


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
'default': {
        dj_database_url.config(default = config('DATABASE_URL'))
        }
}


