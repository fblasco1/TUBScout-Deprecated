from datetime import timedelta
from django.conf import settings
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone

from .utils import random_string_generator, unique_key_generator

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 14)
 
class UsuarioManager(BaseUserManager):
    def crearUsuario(self,email,full_name,tipo_licencia,rol_usuario,id_equipo,password = None):
        if not email:
            raise ValueError('El usuario debe tener correo electrónico!')
        if not password:
            raise ValueError('El usuario debe tener contraseña!')
        usuario = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            tipo_licencia = tipo_licencia,
            rol_usuario = rol_usuario,
            id_equipo = id_equipo,
        )

        self.set_password(password)
        usuario.save()
        return usuario

    def crearAdmin(self,email,username,full_name,tipo_licencia,rol_usuario,id_equipo,password):
        usuario = self.crearUsuario(
                email,
                full_name = full_name,
                password= password,
                tipo_licencia = tipo_licencia,
                rol_usuario = rol_usuario,
                id_equipo = id_equipo,
        )

        self.usuario_administrador = True
        return usuario

LICENCIA_CHOICE = (
    ('B','BASICO'),
    ('P','PRO'),
    ('F','FULL'),
)
ROL_USUARIO_CHOICE = (
    ('E','ENTRENADOR'),
    ('J','JUGADOR'),
    ('A','AGENTE'),
    ('P','PERIODISTA'),
)
class Usuario(AbstractBaseUser):
    email                 = models.EmailField('Correo Electrónico',unique=True,max_length=254)
    full_name             = models.CharField('Nombre Completo', max_length=255, blank=True, null=True)
    tipo_licencia         = models.CharField(max_length=1,choices=LICENCIA_CHOICE)
    rol_usuario           = models.CharField(max_length=1,choices=ROL_USUARIO_CHOICE)
    id_equipo             = models.IntegerField(blank=True, null=True)
    usuario_activo        = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    fecha_registro        = models.DateTimeField('Fecha de creación de licencia', auto_now_add=True)
    
    objects = UsuarioManager()
    

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['rol_usuario','tipo_licencia']

    def __str__(self):
        return f'Usuario: {self.email}'
    
    def get_full_name(self):
        if self.full_name:
            return f'Nombre Completo: {self.full_name}'
        return f'Usuario: {self.email}'

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True

@property
def is_staff(self):
    return self.usuario_administrador

class EmailActivationQuerySet(models.query.QuerySet):
    def confirmacion(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        # does my object have a fecha_registro in here
        end_range = now
        return self.filter(
                activado = False,
                expiracion_forzada = False
              ).filter(
                fecha_alta__gt=start_range,
                fecha_alta__lte=end_range
              )

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmacion(self):
        return self.get_queryset().confirmacion()

    def email_exists(self, email):
        return self.get_queryset().filter(
                    Q(email=email) | 
                    Q(usuario__email=email)
                ).filter(
                    activado=False
                )

class EmailActivation(models.Model):
    usuario             = models.ForeignKey(Usuario,on_delete= models.CASCADE)
    email               = models.EmailField()
    key                 = models.CharField(max_length=120, blank=True, null=True)
    activado            = models.BooleanField(default=False)
    expiracion_forzada  = models.BooleanField(default=False)
    expiracion          = models.IntegerField(default=14) # 14 Days
    fecha_alta          = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmacion() # 1 object
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            # pre activation user signal
            usuario = self.usuario
            usuario.usuario_activo = True
            usuario.save()
            # post activation signal for user
            self.activado = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activado and not self.expiracion_forzada:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', '127.0.0.1:8000')
                key_path = reverse_lazy("usuario:email-activate", kwargs={'key': self.key})
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = '[TUBSCOUT] Verificación de cuenta'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                            subject,
                            txt_,
                            from_email,
                            recipient_list,
                            html_message=html_,
                            fail_silently=False,
                    )
                return sent_mail
        return False


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activado and not instance.expiracion_forzada:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(usuario=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_reciever, sender=Usuario)
