from django.urls import path
from .views import  CalculadoraAvanzada, ListarEquipo, DetalleEquipo, Inicio, DetalleJugador,ListarPartidoEquipo, ListarPartidoJugador, ActualizarJugador

urlpatterns = [
    path('',Inicio.as_view(), name= 'index'),
    path('listar_equipo', ListarEquipo.as_view(), name= 'listar_equipo'),
    #path('cargar_partido',cargarPartido , name='cargar_partido'),
    path('calculator',CalculadoraAvanzada.as_view(), name='calculator'),
    path('detalle_equipo/<int:pk>',DetalleEquipo.as_view(), name='detalle_equipo'),
    path('detalle_partido1/<int:pk>',ListarPartidoEquipo.as_view(), name='detalle_partido1'),
    path('detalle_jugador/<int:pk>',DetalleJugador.as_view(), name='detalle_jugador'),
    path('actualizar_jugador/<int:pk>',ActualizarJugador.as_view(), name='actualizar_jugador'),
    path('detalle_partido2/<int:pk>',ListarPartidoJugador.as_view(), name='detalle_partido2'),
]