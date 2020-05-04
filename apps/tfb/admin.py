from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class JugadoresResources(resources.ModelResource):
    class Meta:
        model = Jugadores

class EquiposResources(resources.ModelResource):
    class Meta:
        model = Equipos

class EquiposAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['nombre_corto']
    list_display =  ('id_equipo','nombre_largo','nombre_corto','zona', 'urlLogo',)
    resource_class = EquiposResources
    
class JugadoresAdmin(ImportExportModelAdmin, admin.ModelAdmin,):
    search_fields = ['id_equipo']
    list_display =  ('id','id_jugador','id_equipo', 'nombre',)
    resource_class = JugadoresResources


admin.site.register(Equipos,EquiposAdmin)
admin.site.register(Jugadores, JugadoresAdmin)
admin.site.register(Partidos)
admin.site.register(Estadistica_Equipo_Partido)
admin.site.register(Estadistica_Jugador_Partido)

