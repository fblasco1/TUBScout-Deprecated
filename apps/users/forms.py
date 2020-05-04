from django import forms
from allauth.account.forms import SignupForm, LoginForm
from apps.tfb.models import Equipos

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

EQUIPOS = []
for equipo in Equipos.objects.all():
    objeto = (equipo.id_equipo,equipo.nombre_corto)
    EQUIPOS.append(objeto)
class CustomSignupForm(SignupForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder':"Correo Electrónico"})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder':"Contraseña"})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder':"Repetir Contraseña"})
        self.fields['first_name']           = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','id':'first_name','placeholder':'Nombres'}))
        self.fields['last_name']            = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','id':'last_name','placeholder':'Apellido'}))
        self.fields['user_type']            = forms.ChoiceField(choices=USER_TYPE,required=True,widget=forms.Select(attrs={'class':'form-control','id':'user_type',}))
        self.fields['coach_team']           = forms.CharField(required=True,widget=forms.Select(attrs={'class':'form-control','id':'coach_team','data-live-search':'True',},choices=EQUIPOS))
        self.fields['license_type']         = forms.ChoiceField(choices=LICENSE_TYPE,required=True,widget=forms.Select(attrs={'class':'form-control', 'id':'license_type'}))
    def save(self, request):
        user_type     = self.cleaned_data.pop('user_type')
        coach_team    = self.cleaned_data.pop('coach_team')
        license_type  = self.cleaned_data.pop('license_type')
        user = super(CustomSignupForm, self).save(request)

class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'input100', 'placeholder':"Correo Electrónico"})
        self.fields['password'].widget.attrs.update({'class': 'input100', 'placeholder':"Contraseña"})
     
    def login(self, *args, **kwargs):
        # You must return the original result.
        return super(CustomLoginForm, self).login(*args, **kwargs)