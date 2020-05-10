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
        TeamA = {'ptsc':int(request.POST['puntoscA']),'tcc':int(request.POST['tccA']),'tci':int(request.POST['tciA']),'T2c':int(request.POST['2PcA']),'T2i':int(request.POST['2PiA']),
        'T3c':int(request.POST['3PcA']),'T3i':int(request.POST['3PiA']), 'TLi':int(request.POST['TLiA']),'RO':int(request.POST['ROA']),'RD':int(request.POST['RDA']),'Asist':int(request.POST['AsistA']),
        'Per':int(request.POST['PerA']),'Rec':int(request.POST['RecA'])}
        #Equipo B
        TeamB = {'ptsc':int(request.POST['puntoscB']),'tcc':int(request.POST['tccB']),'tci':int(request.POST['tciB']),'T2c':int(request.POST['2PcB']), 'T2i':int(request.POST['2PiA']),
        'T3c':int(request.POST['3PcB']), 'T3i':int(request.POST['3PiB']),'TLi':int(request.POST['TLiB']),'RO':int(request.POST['ROB']),'RD':int(request.POST['RDB']),'Asist':int(request.POST['AsistB']),
        'Per':int(request.POST['PerB']),'Rec':int(request.POST['RecB'])}
        #Diccionario Avanzada
        PaceA = StatsAdvance.pace(self,tiroscampointentados= TeamA['tci'],perdidas = TeamA['Per'],tiroslibresintentados = TeamA['TLi'],reboff = TeamA['RO'])
        PaceB = StatsAdvance.pace(self,tiroscampointentados= TeamB['tci'],perdidas = TeamB['Per'],tiroslibresintentados = TeamB['TLi'],reboff = TeamB['RO'])
        avanzada = [
            {'equipo':"A",
            'pace'  :PaceA,
            'ptspos':StatsAdvance.ptspace(self,puntos=TeamA['ptsc'],pace = PaceA),
            'efg'   :StatsAdvance.efFG(self,doblesconvertidos = TeamA['T2c'],triplesconvertidos = TeamA['T3c'],tiroscampointentados=TeamA['tci']),
            'ts'    :StatsAdvance.ts(self,puntos=TeamA['ptsc'],tiroscampointentados=TeamA['tci'],tiroslibresintentados=TeamA['TLi']),
            'efoff' :StatsAdvance.effOff(self,puntos=TeamA['ptsc'],pace=PaceA),
            'efdef' :StatsAdvance.effDef(self,puntosrival=TeamB['ptsc'],pace=PaceB),
            'tcas'  :StatsAdvance.tTCAS(self,tiroscampoconvertidos=TeamA['tcc'],asistencias=TeamA['Asist']),
            'tro'   :StatsAdvance.tRO(self,rebof=TeamA['RO'],rebdef=TeamA['RD']),
            'trd'   :StatsAdvance.tRD(self,rebdef=TeamA['RD'],reboff=TeamA['RO']),
            'tas'   :StatsAdvance.tAS(self,asistencias=TeamA['Asist'],pace=PaceA),
            'asper' :StatsAdvance.tASPER(self,asistencias=TeamA['Asist'],perdidas=TeamA['Per']),
            'trec'  :StatsAdvance.tREC(self,recuperos=TeamA['Rec'],pace=PaceA),
            'tper'  :StatsAdvance.tPER(self,perdidas=TeamA['Per'],pace=PaceA),
            'optl'  :StatsAdvance.VTLTC(self,tiroslibresintentados=TeamA['TLi'],tiroscampointentados=TeamA['tci']),
            'v2p'   :StatsAdvance.V2PTC(self,doblesintentados=TeamA['T2i'],tiroscampointentados=TeamA['tci']),
            'v3p'   :StatsAdvance.V3PTC(self,triplesintentados=TeamA['T3i'],tiroscampointentados=TeamA['tci'])},
            {'equipo':"B",
             'pace'  :PaceB,
             'ptspos':StatsAdvance.ptspace(self,puntos=TeamB['ptsc'],pace = PaceB),
             'efg'   :StatsAdvance.efFG(self,doblesconvertidos = TeamB['T2c'],triplesconvertidos =TeamB['T3c'],tiroscampointentados=TeamB['tci']),
             'ts'    :StatsAdvance.ts(self,puntos=TeamB['ptsc'],tiroscampointentados=TeamB['tci'],tiroslibresintentados=TeamB['TLi']),
             'efoff' :StatsAdvance.effOff(self,puntos=TeamB['ptsc'],pace=PaceB),
             'efdef' :StatsAdvance.effDef(self,puntosrival=TeamA['ptsc'],pace=PaceA),
             'tcas'  :StatsAdvance.tTCAS(self,tiroscampoconvertidos=TeamB['tcc'],asistencias=TeamB['Asist']),
             'tro'   :StatsAdvance.tRO(self,rebof=TeamB['RO'],rebdef=TeamB['RD']),
             'trd'   :StatsAdvance.tRD(self,rebdef=TeamB['RD'],reboff=TeamB['RO']),
             'tas'   :StatsAdvance.tAS(self,asistencias=TeamB['Asist'],pace=PaceB),
             'asper' :StatsAdvance.tASPER(self,asistencias=TeamB['Asist'],perdidas=TeamB['Per']),
             'trec'  :StatsAdvance.tREC(self,recuperos=TeamB['Rec'],pace=PaceB),
             'tper'  :StatsAdvance.tPER(self,perdidas=TeamB['Per'],pace=PaceB),
             'optl'  :StatsAdvance.VTLTC(self,tiroslibresintentados=TeamB['TLi'],tiroscampointentados=TeamB['tci']),
             'v2p'   :StatsAdvance.V2PTC(self,doblesintentados=TeamB['T2i'],tiroscampointentados=TeamB['tci']),
             'v3p'   :StatsAdvance.V3PTC(self,triplesintentados=TeamB['T3i'],tiroscampointentados=TeamB['tci'])},
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
        contexto['estadisticas'] = Estadistica_Equipo_Partido.objects.filter(id_equipo= self.kwargs['pk']).aggregate(
                                                                                            puntos = Avg('puntos'),
                                                                                            q1     = Avg('q1'),
                                                                                            q2     = Avg('q2'),
                                                                                            q3     = Avg('q3'),
                                                                                            q4     = Avg('q4'),
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
                                                                                            ptsxpace = Avg('ptsxpace'),
                                                                                            eficiencia_tiro_campo = Avg('eficiencia_tiro_campo'),
                                                                                            true_shooting = Avg('true_shooting'),
                                                                                            eficiencia_ofensiva = Avg('eficiencia_ofensiva'),
                                                                                            eficiencia_defensiva = Avg('eficiencia_defensiva'),
                                                                                            tiros_campo_asistidos = Avg('tiros_campo_asistidos'),
                                                                                            tasa_rebote_ofensivo = Avg('tasa_rebote_ofensivo'),
                                                                                            tasa_rebote_defensivo = Avg('tasa_rebote_defensivo'),
                                                                                            tasa_recuperos = Avg('tasa_recuperos'),
                                                                                            tasa_asistencias = Avg('tasa_asistencias'),
                                                                                            tasa_perdidas = Avg('tasa_perdidas'),
                                                                                            tasa_as_per = Avg('tasa_as_per'),
                                                                                            tasa_tapones = Avg('tasa_tapones'),
                                                                                            tl_rate = Avg('tl_rate'),
                                                                                            p2_rate = Avg('p2_rate'),
                                                                                            p3_rate = Avg('p3_rate'),
                                                                                            puntos_de_perdidas = Avg('puntos_de_perdidas'),
                                                                                            puntos_pintura = Avg('puntos_pintura'),
                                                                                            puntos_contraataque = Avg('puntos_contraataque'),
                                                                                            puntos_banca = Avg('puntos_banca'),
                                                                                            puntos_ro = Avg('puntos_ro'),
                                                                                            ganados = Count("pk",filter= Q(partido_ganado=1 )),
                                                                                            perdidos = Count("pk",filter= Q(partido_ganado=0)),
                                                                                            ganloc  = Count("pk",filter= Q(partido_ganado=1) & Q(localia='1')),
                                                                                            perloc = Count("pk",filter= Q(partido_ganado=0) & Q(localia='1')),
                                                                                            ganvis = Count("pk",filter= Q(partido_ganado=1) & Q(localia='0')),
                                                                                            pervis = Count("pk",filter= Q(partido_ganado=0) & Q(localia='0')),
                                                                                            )
        contexto['plantel']     = Jugadores.objects.filter(id_equipo = self.kwargs['pk'], estado = "A")
        contexto['equipo']      = Equipos.objects.get(id_equipo = self.kwargs['pk'])
        contexto['partidos']    = Estadistica_Equipo_Partido.objects.filter(id_equipo = self.kwargs['pk'])
        a = 0
        for partido in contexto['partidos']:
           contexto['partidos'][a].equiporival = Estadistica_Equipo_Partido.objects.filter(id_partido = partido.id_partido).exclude(id_equipo = self.kwargs['pk']).get()
           a = a + 1 
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())

class DetalleJugador(ListView):
    template_name= 'tfb/detalle_jugador.html'

    def get_queryset(self): 
        return Estadistica_Jugador_Partido.objects.filter(id_jugador= self.kwargs['idp']).aggregate(puntos = Avg('puntos'),
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
                                                                                       usg = Avg('usg'),
                                                                                       eficiencia_ofensiva = Avg('eficiencia_ofensiva'),
                                                                                       eficiencia_tiro_campo = Avg('eficiencia_tiro_campo'),
                                                                                       true_shooting = Avg('true_shooting'),
                                                                                       tasa_asistencias = Avg('tasa_asistencias'),
                                                                                       tasa_as_per = Avg('tasa_as_per'),
                                                                                       tasa_perdidas = Avg('tasa_perdidas'),
                                                                                       tasa_recuperos = Avg('tasa_recuperos'),
                                                                                       tl_rate = Avg('tl_rate'),
                                                                                       p2_rate = Avg('p2_rate'),
                                                                                       p3_rate = Avg('p3_rate'),                                                 
                                                                                       inicial = Count("pk", filter = Q(inicial=1)),
                                                                                       cant_partidos = Count("pk"),
                                                                                    )

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['equipo']       = Equipos.objects.get(id_equipo = self.kwargs['ide'])
        contexto['estadisticas'] = Estadistica_Equipo_Partido.objects.filter(id_equipo= self.kwargs['ide']).aggregate(
                                                                                            puntos = Avg('puntos'),
                                                                                            q1     = Avg('q1'),
                                                                                            q2     = Avg('q2'),
                                                                                            q3     = Avg('q3'),
                                                                                            q4     = Avg('q4'),
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
                                                                                            ptsxpace = Avg('ptsxpace'),
                                                                                            eficiencia_tiro_campo = Avg('eficiencia_tiro_campo'),
                                                                                            true_shooting = Avg('true_shooting'),
                                                                                            eficiencia_ofensiva = Avg('eficiencia_ofensiva'),
                                                                                            eficiencia_defensiva = Avg('eficiencia_defensiva'),
                                                                                            tiros_campo_asistidos = Avg('tiros_campo_asistidos'),
                                                                                            tasa_rebote_ofensivo = Avg('tasa_rebote_ofensivo'),
                                                                                            tasa_rebote_defensivo = Avg('tasa_rebote_defensivo'),
                                                                                            tasa_recuperos = Avg('tasa_recuperos'),
                                                                                            tasa_asistencias = Avg('tasa_asistencias'),
                                                                                            tasa_perdidas = Avg('tasa_perdidas'),
                                                                                            tasa_as_per = Avg('tasa_as_per'),
                                                                                            tasa_tapones = Avg('tasa_tapones'),
                                                                                            tl_rate = Avg('tl_rate'),
                                                                                            p2_rate = Avg('p2_rate'),
                                                                                            p3_rate = Avg('p3_rate'),
                                                                                            puntos_de_perdidas = Avg('puntos_de_perdidas'),
                                                                                            puntos_pintura = Avg('puntos_pintura'),
                                                                                            puntos_contraataque = Avg('puntos_contraataque'),
                                                                                            puntos_banca = Avg('puntos_banca'),
                                                                                            puntos_ro = Avg('puntos_ro'),
                                                                                            ganados = Count("pk",filter= Q(partido_ganado=1 )),
                                                                                            perdidos = Count("pk",filter= Q(partido_ganado=0)),
                                                                                            ganloc  = Count("pk",filter= Q(partido_ganado=1) & Q(localia='1')),
                                                                                            perloc = Count("pk",filter= Q(partido_ganado=0) & Q(localia='1')),
                                                                                            ganvis = Count("pk",filter= Q(partido_ganado=1) & Q(localia='0')),
                                                                                            pervis = Count("pk",filter= Q(partido_ganado=0) & Q(localia='0')),
                                                                                            )
        contexto['playerstats']  = self.get_queryset()
        contexto['plantel']      = Jugadores.objects.filter(id_equipo = self.kwargs['ide'], estado = "A")
        contexto['partidos']     = Estadistica_Equipo_Partido.objects.filter(id_equipo = self.kwargs['ide'])
        contexto['player']       = Jugadores.objects.filter(id = self.kwargs['idp']).get()
        a = 0
        for partido in contexto['partidos']:
           contexto['partidos'][a].equiporival = Estadistica_Equipo_Partido.objects.filter(id_partido = partido.id_partido).exclude(id_equipo = self.kwargs['ide']).get()
           a = a + 1 
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

