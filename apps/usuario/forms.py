from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

Usuario = get_user_model()

from apps.tfb.models import Equipos
from .models import EmailActivation

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

class ReactivateEmailForm(forms.Form):
    email       = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email) 
        if not qs.exists():
            register_link = reverse_lazy('registro')
            msg = """Este email es inexistente, desea ir a <a href="{link}">registrarse</a>?
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('full_name', 'email','tipo_licencia','rol_usuario','id_equipo')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas deben coincidir")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        usuario = super(UserAdminCreationForm, self).save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])
        if commit:
            usuario.save()
        return usuario

class UserDetailChangeForm(forms.ModelForm):
    full_name = forms.CharField(label='Nombre Completo', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    id_equipo = forms.IntegerField()
    
    class Meta:
        model = Usuario
        fields = ['full_name','id_equipo']

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model  = Usuario
        fields = ('full_name', 'email','id_equipo','password', 'usuario_activo', 'usuario_administrador')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class LoginForm(forms.Form):
    email    = forms.CharField(label='Correo Electrónico', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Correo Electrónico'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data    = self.cleaned_data
        email   = data.get('email')
        password= data.get("password")
        qs = EmailActivation.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check active/
            no_activado = qs.filter(activado=False)
            if no_activado.exists():
                ## not active, check email activation
                link = reverse_lazy("usuario:resend-activation")
                reconfirm_msg = """Haga click aquí <a href='{resend_link}'>
                para reenviar la confirmación de email</a>.
                """.format(resend_link = link)
                confirmar_email = EmailActivation.objects.filter(email=email)
                esta_confirmado = confirmar_email.confirmacion().exists()
                if esta_confirmado:
                    msg1 = "Por favor verifique su email para confirmar su cuenta " + reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_existente = EmailActivation.objects.email_exists(email).exists()
                if email_existente:
                    msg2 = "Email no confirmado. " + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not esta_confirmado and not email_existente:
                    raise forms.ValidationError("Este usuario no está activado")
        usuario = authenticate(request, email=email, password=password)
        if usuario is None:
            raise forms.ValidationError("Credenciales inválidas.")
        login(request, usuario)
        self.usuario = usuario
        return data

class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label="Contraseña",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirmar Contraseña",widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = Usuario
        fields = ('full_name', 'email','id_equipo','tipo_licencia','rol_usuario')
        labels = {
            'full_name':'Nombre Completo',
            'email':'Correo Electrónico',
            'id_equipo':'Equipo',
            'tipo_licencia':'Tipo de Licencia',
            'rol_usuario':'Rol'
        }
        widgets ={
            'full_name':forms.TextInput(
                attrs={
                    'class':'form-control',
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'class':'form-control',
                    }
            ),
            'id_equipo':forms.Select(
                attrs={
                    'class':'form-control',
                    'choices':Equipos.objects.all(),
                    'id':'equipo_name'
                    }
            ),
            'rol_usuario':forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'rol_usuario',
                    }
            ),
            'tipo_licencia':forms.Select(
                attrs={
                    'class':'form-control',
                    'id':'tipo_licencia',
                    }
            ),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas deben coincidir")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        usuario = super(RegisterForm, self).save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])
        usuario.activado = False # send confirmation email via signals
        # obj = EmailActivation.objects.create(user=user)
        # obj.send_activation_email()
        if commit:
            usuario.save()
        return usuario
