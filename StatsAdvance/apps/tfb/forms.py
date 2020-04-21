from django import forms
from .models import Jugadores,Equipos

class DetalleJugadorForm(forms.ModelForm):
    class Meta:
        model = Jugadores
        fields = ['nombre','id_equipo','id_jugador','estado']
        labels ={
            'nombre':'Nombre del Jugador',
            'id_equipo':'Equipo',
            'id_jugador': 'Código Jugador-Equipo',
            'estado': 'Estado',
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'j_nombre',
                }
            ),
            """
            'id_equipo': forms.Select(
                attrs={
                    'class':'form-control'
                },
                choices= Equipos.objects.all()
            ),
            """
            'id_jugador': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'pno',
                }
            ),
            'estado': forms.Select(
                attrs={
                    'class':'form-control',
                }
            ),
        }

