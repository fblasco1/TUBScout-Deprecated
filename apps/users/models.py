from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

USER_TYPE = [
    ('E','ENTRENADOR'),
    ('A','AGENTE'),
    ('J','JUGADOR'),
    ('P','PERIODISTA'),
]

LICENSE_TYPE = [
    ('B','BASIC'),
    ('P','PRO'),
    ('F','FULL'),
]

class CustomUser(AbstractUser):
    username        = None
    email           = models.EmailField(_('email address'), unique=True)
    first_name      = models.CharField(max_length=100,null=True,blank=True)
    last_name       = models.CharField(max_length=100,null=True,blank=True)
    user_type       = models.CharField(max_length=40,choices=USER_TYPE)
    coach_team      = models.CharField(max_length=255,null=True, blank=True)
    license_type    = models.CharField(max_length=40,choices=LICENSE_TYPE)
    expiration      = models.BooleanField(default=False)
    creation_date   = models.DateTimeField(auto_now_add=True)    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type','license_type']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email