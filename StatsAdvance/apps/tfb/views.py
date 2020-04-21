from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.db.models import Sum,Avg, Q, Count, F, Case, When, Subquery
from .models import Equipos,Jugadores, Estadistica_Equipo_Partido, Estadistica_Jugador_Partido, Partidos
from .forms import DetalleJugadorForm
from TUBSClass import StatsAdvance


class Inicio(TemplateView):
    template_name = 'tfb/home.html'

class CalculadoraAvanzada(View):
    template_name = 'tfb/calculator.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        #Equipo A
        TeamA = {'ptsc':int(request.POST['puntoscA']),'ptsr':int(request.POST['puntosrA']),'tci':int(request.POST['tciA']),'T2c':int(request.POST['2PcA']),'T3c':int(request.POST['3PcA']),        
        'TLi':int(request.POST['TLiA']),'RO':int(request.POST['ROA']),'RD':int(request.POST['RDA']),'Asist':int(request.POST['AsistA']),'Per':int(request.POST['PerA']),'Rec':int(request.POST['RecA'])}
        #Equipo B
        TeamB = {'ptsc':int(request.POST['puntoscB']),'ptsr':int(request.POST['puntosrB']),'tci':int(request.POST['tciB']),'T2c':int(request.POST['2PcB']),'T3c':int(request.POST['3PcB']),        
        'TLi':int(request.POST['TLiB']),'RO':int(request.POST['ROB']),'RD':int(request.POST['RDB']),'Asist':int(request.POST['AsistB']),'Per':int(request.POST['PerB']),'Rec':int(request.POST['RecB'])}
        #Diccionario Avanzada
        PaceA = StatsAdvance.pace(self,tiroscampointentados= TeamA['tci'],perdidas = TeamA['Per'],tiroslibresintentados = TeamA['TLi'],reboff = TeamA['RO'])
        PaceB = StatsAdvance.pace(self,tiroscampointentados= TeamB['tci'],perdidas = TeamB['Per'],tiroslibresintentados = TeamB['TLi'],reboff = TeamB['RO'])
        avanzada = [
            {'equipo':"A",
            'pace' :PaceA,
            'ptspos':StatsAdvance.ptspace(self,puntos=TeamA['ptsc'],pace = PaceA),
            'efg'   :StatsAdvance.efFG(self,doblesconvertidos = TeamA['T2c'],triplesconvertidos = TeamA['T3c'],tiroscampointentados=TeamA['tci']),
            'ts'    :StatsAdvance.ts(self,puntos=TeamA['ptsc'],tiroscampointentados=TeamA['tci'],tiroslibresintentados=TeamA['TLi']),
            'efoff' :StatsAdvance.effOff(self,puntos=TeamA['ptsc'],pace=PaceA),
            'efdef' :StatsAdvance.effDef(self,puntosrival=TeamA['ptsr'],pace=PaceB),
            'tro'   :StatsAdvance.tRO(self,rebof=TeamA['RO'],rebdef=TeamA['RD']),
            'trd'   :StatsAdvance.tRD(self,rebdef=TeamA['RD'],reboff=TeamA['RO']),
            'tas'   :StatsAdvance.tAS(self,asistencias=TeamA['Asist'],pace=PaceA),
            'asper':StatsAdvance.tASPER(self,asistencias=TeamA['Asist'],perdidas=TeamA['Per']),
            'trec'  :StatsAdvance.tREC(self,recuperos=TeamA['Rec'],pace=PaceA),
            'tper'  :StatsAdvance.tPER(self,perdidas=TeamA['Per'],pace=PaceA),
            'optl'  :StatsAdvance.opTL(self,tiroslibresconvertidos=TeamA['TLi'],tiroscampointentados=TeamA['tci'])},
            {'equipo':"B",
             'pace'  :PaceB,
             'ptspos':StatsAdvance.ptspace(self,puntos=TeamB['ptsc'],pace = PaceB),
             'efg'   :StatsAdvance.efFG(self,doblesconvertidos = TeamB['T2c'],triplesconvertidos =TeamB['T3c'],tiroscampointentados=TeamB['tci']),
             'ts'    :StatsAdvance.ts(self,puntos=TeamB['ptsc'],tiroscampointentados=TeamB['tci'],tiroslibresintentados=TeamB['TLi']),
             'efoff' :StatsAdvance.effOff(self,puntos=TeamB['ptsc'],pace=PaceB),
             'efdef' :StatsAdvance.effDef(self,puntosrival=TeamB['ptsr'],pace=PaceA),
             'tro'   :StatsAdvance.tRO(self,rebof=TeamB['RO'],rebdef=TeamB['RD']),
             'trd'   :StatsAdvance.tRD(self,rebdef=TeamB['RD'],reboff=TeamB['RO']),
             'tas'   :StatsAdvance.tAS(self,asistencias=TeamB['Asist'],pace=PaceB),
             'asper':StatsAdvance.tASPER(self,asistencias=TeamB['Asist'],perdidas=TeamB['Per']),
             'trec'  :StatsAdvance.tREC(self,recuperos=TeamB['Rec'],pace=PaceB),
             'tper'  :StatsAdvance.tPER(self,perdidas=TeamB['Per'],pace=PaceB),
             'optl'  :StatsAdvance.opTL(self,tiroslibresconvertidos=TeamB['TLi'],tiroscampointentados=TeamB['tci'])}
             ]

        return render(request, self.template_name, {'avanzadas': avanzada})

class ListarEquipo(ListView):
    model = Equipos
    template_name = 'tfb/equipos.html'
    context_object_name = 'Equipos'
    queryset = Equipos.objects.filter()

class DetalleEquipo(ListView):
    template_name = 'tfb/detalle_equipo.html'

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['estadisticas'] = Estadistica_Equipo_Partido.objects.filter(id_equipo= self.kwargs['pk']).aggregate(puntos = Avg('puntos'),
                                                                                            tiros_campo_convertidos = Sum('tiros_campo_convertidos'),
                                                                                            tiros_campo_intentados = Sum('tiros_campo_intentados'),
                                                                                            tiros_campo_porcentaje = Case(
                                                                                                                         When(tiros_campo_intentados = 0, then = 0),
                                                                                                                         default = Sum('tiros_campo_convertidos') * 100/Sum('tiros_campo_intentados')),
                                                                                            tiros_2_convertidos = Sum('tiros_2_convertidos'),
                                                                                            tiros_2_intentados = Sum('tiros_2_intentados'),
                                                                                            tiros_2_porcentaje = Case(
                                                                                                                    When(tiros_2_intentados = 0, then = 0),
                                                                                                                    default = Sum('tiros_2_convertidos') * 100/Sum('tiros_2_intentados')),
                                                                                            tiros_3_convertidos = Sum('tiros_3_convertidos'),
                                                                                            tiros_3_intentados = Sum('tiros_3_intentados'),
                                                                                            tiros_3_porcentaje = Case(
                                                                                                                    When(tiros_3_intentados=0, then = 0),
                                                                                                                    default = Sum('tiros_3_convertidos')* 100 /Sum('tiros_3_intentados')),
                                                                                            tiro_libre_convertido = Sum('tiro_libre_convertido'),
                                                                                            tiro_libre_intentado = Sum('tiro_libre_intentado'),
                                                                                            tiros_libre_porcentaje = Case(
                                                                                                                        When(tiro_libre_intentado = 0, then= 0),
                                                                                                                        default = Sum('tiro_libre_convertido')*100/Sum('tiro_libre_intentado')),
                                                                                            rebote_ofensivo = Avg('rebote_ofensivo'),
                                                                                            rebote_defensivo = Avg('rebote_defensivo'),                                                                
                                                                                            rebote_total = Avg('rebote_total'),
                                                                                            asistencias = Avg('asistencias'),
                                                                                            perdidas = Avg('perdidas'),
                                                                                            recuperos = Avg('recuperos'),
                                                                                            tapones = Avg('tapones'),
                                                                                            faltas_personales = Avg('faltas_personales'),                                                                
                                                                                            valoración = Avg('valoración'),
                                                                                            pace = Avg('pace'),
                                                                                            eficiencia_tiro_campo = Avg('eficiencia_tiro_campo'),
                                                                                            true_shooting = Avg('true_shooting'),
                                                                                            eficiencia_ofensiva = Avg('eficiencia_ofensiva'),
                                                                                            eficiencia_defensiva = Avg('eficiencia_defensiva'),
                                                                                            tasa_rebote_ofensivo = Avg('tasa_rebote_ofensivo'),
                                                                                            tasa_rebote_defensivo = Avg('tasa_rebote_defensivo'),
                                                                                            tasa_recuperos = Avg('tasa_recuperos'),
                                                                                            tasa_asistencias = Avg('tasa_asistencias'),
                                                                                            tasa_perdidas = Avg('tasa_perdidas'),
                                                                                            oportunidad_tiro_libre = Avg('oportunidad_tiro_libre'),
                                                                                            puntos_de_perdidas = Avg('puntos_de_perdidas'),
                                                                                            puntos_pintura = Avg('puntos_pintura'),
                                                                                            puntos_contraataque = Avg('puntos_contraataque'),
                                                                                            puntos_banca = Avg('puntos_banca'),
                                                                                            ganados = Count("pk",filter= Q(partido_ganado=1)),
                                                                                            perdidos = Count("pk",filter= Q(partido_ganado=0)),
                                                                                            )
        contexto['plantel'] = Jugadores.objects.filter(id_equipo = self.kwargs['pk'], estado = "A")
        contexto['equipo'] = Equipos.objects.get(id_equipo = self.kwargs['pk'])
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())

class ListarPartidoEquipo(ListView):
    template_name = 'tfb/detalle_partido.html'
    context_object_name = 'partidosEquipo'
    
    def get_queryset(self):
        partidos = Estadistica_Equipo_Partido.objects.filter(id_equipo = self.kwargs['pk'])
        a = 0
        for partido in partidos:
           partidos[a].equiporival = Estadistica_Equipo_Partido.objects.filter(id_partido = partido.id_partido).exclude(id_equipo = self.kwargs['pk']).get().id_equipo
           a = a + 1 
        return partidos

class DetalleJugador(ListView):
    template_name= 'tfb/detalle_jugador.html'

    def get_queryset(self): 
        return Estadistica_Jugador_Partido.objects.filter(id_jugador= self.kwargs['pk']).aggregate(puntos = Avg('puntos'),
                                                                                       minutos = Avg(F('minutos')),
                                                                                       tiros_campo_convertidos = Sum('tiros_campo_convertidos'),
                                                                                       tiros_campo_intentados = Sum('tiros_campo_intentados'),
                                                                                       tiros_campo_porcentaje = Case(
                                                                                                                When(tiros_campo_intentados = 0, then =0),
                                                                                                                default= Sum('tiros_campo_convertidos') * 100/Sum('tiros_campo_intentados'),
                                                                                       ),
                                                                                       tiros_2_convertidos = Sum('tiros_2_convertidos'),
                                                                                       tiros_2_intentados = Sum('tiros_2_intentados'),
                                                                                       tiros_2_porcentaje = Case(
                                                                                                                When (tiros_2_intentados = 0, then =0),
                                                                                                                default= Sum('tiros_2_convertidos') * 100/Sum('tiros_2_intentados'),
                                                                                       ),
                                                                                       tiros_3_convertidos = Sum('tiros_3_convertidos'),
                                                                                       tiros_3_intentados = Sum('tiros_3_intentados'),
                                                                                       tiros_3_porcentaje = Case(
                                                                                                                When (tiros_3_intentados = 0, then =0),
                                                                                                                default= Sum('tiros_3_convertidos') * 100/Sum('tiros_3_intentados'),
                                                                                       ),
                                                                                       tiro_libre_convertido = Sum('tiro_libre_convertido'),
                                                                                       tiro_libre_intentado = Sum('tiro_libre_intentado'),
                                                                                       tiros_libre_porcentaje = Case(
                                                                                                                When (tiro_libre_intentado = 0, then =0),
                                                                                                                default= Sum('tiro_libre_convertido') * 100/Sum('tiro_libre_intentado'),
                                                                                       ),
                                                                                       rebote_ofensivo = Avg('rebote_ofensivo'),
                                                                                       rebote_defensivo = Avg('rebote_defensivo'),                                                                
                                                                                       rebote_total = Avg('rebote_total'),
                                                                                       asistencias = Avg('asistencias'),
                                                                                       perdidas = Avg('perdidas'),
                                                                                       recuperos = Avg('recuperos'),
                                                                                       tapones = Avg('tapones'),
                                                                                       faltas_personales = Avg('faltas_personales'),
                                                                                       diferencia_puntos = Avg('diferencia_puntos'),                                                                
                                                                                       valoración = Avg('valoración'),
                                                                                       pace = Avg('pace'),
                                                                                       ptspace = Avg('ptspace'),
                                                                                       effOf = Avg('effOf'),
                                                                                       efFG = Avg('efFG'),
                                                                                       ts = Avg('ts'),
                                                                                       tas = Avg('tas'),
                                                                                       asper = Avg('asper'),
                                                                                       tper = Avg('tper'),
                                                                                       trec = Avg('trec'),
                                                                                       opTL = Avg('opTL'),                                                 
                                                                                    )

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['estadisticas'] = self.get_queryset()
        contexto['jugador'] = Jugadores.objects.get(id = self.kwargs['pk'])
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())

class ListarPartidoJugador(ListView):
    template_name = 'tfb/detalle_partido.html'
    context_object_name = 'partidosJugador'

    def get_queryset(self):
        partidos = Estadistica_Jugador_Partido.objects.filter(id_jugador = self.kwargs['pk'])
        a = 0
        for partido in partidos:
           partidos[a].equiporival = Estadistica_Equipo_Partido.objects.filter(id_partido = partido.id_partido).exclude(id_equipo = partido.id_jugador.id_equipo).get().id_equipo
           a = a + 1 
        return partidos

class ActualizarJugador(UpdateView):
    model = Jugadores
    form_class = DetalleJugadorForm
    template_name = 'tfb/md-jugador.html'
    
    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        return contexto

    def get_success_url(self):
        return reverse_lazy('tfb:detalle_jugador',kwargs = {'pk': self.kwargs['pk']})

