from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.db.models import Sum,Avg, Q, Count, F, Case, When, Subquery, FloatField
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
                                                                                            tiros_campo_convertidos     = Sum('tiros_campo_convertidos'),
                                                                                            p_tiros_campo_convertidos   = Avg('tiros_campo_convertidos'),                                           
                                                                                            tiros_campo_intentados      = Sum('tiros_campo_intentados'),
                                                                                            p_tiros_campo_intentados    = Avg('tiros_campo_intentados'),
                                                                                            tiros_campo_porcentaje      = Case(
                                                                                                                         When(tiros_campo_intentados = 0, then = 0),
                                                                                                                         default = Sum('tiros_campo_convertidos') * 100/Sum('tiros_campo_intentados')),
                                                                                            tiros_2_convertidos         = Sum('tiros_2_convertidos'),
                                                                                            p_tiros_2_convertidos       = Avg('tiros_2_convertidos'),  
                                                                                            tiros_2_intentados          = Sum('tiros_2_intentados'),
                                                                                            p_tiros_2_intentados        = Avg('tiros_2_intentados'),
                                                                                            tiros_2_porcentaje          = Case(
                                                                                                                         When(tiros_2_intentados = 0, then = 0),
                                                                                                                         default = Sum('tiros_2_convertidos') * 100/Sum('tiros_2_intentados')),
                                                                                            tiros_3_convertidos = Sum('tiros_3_convertidos'),
                                                                                            p_tiros_3_convertidos = Avg('tiros_3_convertidos'),
                                                                                            tiros_3_intentados = Sum('tiros_3_intentados'),
                                                                                            p_tiros_3_intentados = Avg('tiros_3_intentados'),
                                                                                            tiros_3_porcentaje = Case(
                                                                                                                    When(tiros_3_intentados=0, then = 0),
                                                                                                                    default = Sum('tiros_3_convertidos')* 100 /Sum('tiros_3_intentados')),
                                                                                            tiro_libre_convertido = Sum('tiro_libre_convertido'),
                                                                                            p_tiro_libre_convertido = Avg('tiro_libre_convertido'),
                                                                                            tiro_libre_intentado = Sum('tiro_libre_intentado'),
                                                                                            p_tiro_libre_intentado = Avg('tiro_libre_intentado'),
                                                                                            tiros_libre_porcentaje = Case(
                                                                                                                        When(tiro_libre_intentado = 0, then= 0),
                                                                                                                        default = Sum('tiro_libre_convertido')*100/Sum('tiro_libre_intentado')),
                                                                                            rebote_ofensivo = Sum('rebote_ofensivo'),
                                                                                            p_rebote_ofensivo = Avg('rebote_ofensivo'),
                                                                                            rebote_defensivo = Sum('rebote_defensivo'),
                                                                                            p_rebote_defensivo = Avg('rebote_defensivo'),                                                                
                                                                                            rebote_total = Sum('rebote_total'),
                                                                                            p_rebote_total = Avg('rebote_total'),
                                                                                            asistencias = Sum('asistencias'),
                                                                                            p_asistencias = Avg('asistencias'),
                                                                                            perdidas = Sum('perdidas'),
                                                                                            p_perdidas = Avg('perdidas'),
                                                                                            recuperos = Sum('recuperos'),
                                                                                            p_recuperos = Avg('recuperos'),
                                                                                            tapones = Sum('tapones'),
                                                                                            p_tapones = Avg('tapones'),
                                                                                            faltas_personales = Sum('faltas_personales'),
                                                                                            p_faltas_personales = Avg('faltas_personales'),                                                                
                                                                                            valoración = Sum('valoración'),
                                                                                            p_valoración = Avg('valoración'),
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
        contexto['plantel']         = Jugadores.objects.filter(id_equipo = self.kwargs['pk'], estado = "A")
        contexto['equipo']          = Equipos.objects.get(id_equipo = self.kwargs['pk'])
        contexto['partidos']        = Estadistica_Equipo_Partido.objects.filter(id_equipo = self.kwargs['pk'])
        contexto['quinteto']        = Estadistica_Jugador_Partido.objects.filter(id_partido__estadistica_equipo_partido__id_equipo = self.kwargs['pk'],id_jugador__id_equipo = self.kwargs['pk'], inicial = 1).order_by('-id_partido__detalle_partido')[:5]
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
                                                                                       pace    =  (Sum('tiros_campo_intentados',output_field=FloatField()) + Sum('perdidas',output_field=FloatField()) + 0.44 * (Sum('tiro_libre_intentado',output_field=FloatField())-Sum('rebote_ofensivo',output_field=FloatField()))) / Count("pk",output_field=FloatField())  ,
                                                                                       ptspace =  (Sum('puntos',output_field=FloatField()) / ((Sum('tiros_campo_intentados',output_field=FloatField()) + Sum('perdidas',output_field=FloatField()) + 0.44 * (Sum('tiro_libre_intentado',output_field=FloatField())-Sum('rebote_ofensivo',output_field=FloatField()))) / Count("pk",output_field=FloatField()))) / Count("pk",output_field=FloatField()),
                                                                                       #ptsmin  =  (Sum('puntos',output_field=FloatField()) / Sum(F('minutos'),output_field=FloatField())) / Count("pk",output_field=FloatField()),
                                                                                       ptstl = Sum('tiro_libre_convertido') / Sum('tiro_libre_intentado'),
                                                                                       pts2p = (Sum('tiros_2_convertidos') * 2)/Sum('tiros_2_intentados'),
                                                                                       pts3p = (Sum('tiros_3_convertidos') * 3)/Sum('tiros_3_intentados'),
                                                                                       usg = Avg('usg'),
                                                                                       eficiencia_ofensiva =  ((Sum('puntos',output_field=FloatField()) / ((Sum('tiros_campo_intentados',output_field=FloatField()) + Sum('perdidas',output_field=FloatField()) + 0.44 * (Sum('tiro_libre_intentado',output_field=FloatField())-Sum('rebote_ofensivo',output_field=FloatField()))) / Count("pk",output_field=FloatField()))) / Count("pk",output_field=FloatField())) * 100,
                                                                                       eficiencia_tiro_campo = (Sum('tiros_2_convertidos',output_field=FloatField()) + 0.5 * Sum('tiros_3_convertidos',outputfield=FloatField())) / Sum('tiros_campo_intentados',output_field=FloatField()) * 100,
                                                                                       true_shooting = (Sum('puntos',output_field=FloatField())/ (2 * (Sum('tiros_campo_intentados',output_field=FloatField()) + 0.44 * Sum('tiro_libre_intentado',output_field=FloatField())))) *100,
                                                                                       tasa_asistencias = ((Sum('asistencias',output_field=FloatField())/ ((Sum('tiros_campo_intentados',output_field=FloatField()) + Sum('perdidas',output_field=FloatField()) + 0.44 * (Sum('tiro_libre_intentado',output_field=FloatField())-Sum('rebote_ofensivo',output_field=FloatField()))) / Count("pk",output_field=FloatField()))*100) / Count("pk",output_field=FloatField())),
                                                                                       tasa_as_per = (Sum('asistencias',output_field=FloatField())/ Sum('perdidas',output_field=FloatField())),
                                                                                       tasa_perdidas = ((Sum('perdidas',output_field=FloatField())/ ((Sum('tiros_campo_intentados',output_field=FloatField()) + Sum('perdidas',output_field=FloatField()) + 0.44 * (Sum('tiro_libre_intentado',output_field=FloatField())-Sum('rebote_ofensivo',output_field=FloatField()))) / Count("pk",output_field=FloatField()))*100) / Count("pk",output_field=FloatField())),
                                                                                       tasa_recuperos = ((Sum('recuperos',output_field=FloatField())/ ((Sum('tiros_campo_intentados',output_field=FloatField()) + Sum('perdidas',output_field=FloatField()) + 0.44 * (Sum('tiro_libre_intentado',output_field=FloatField())-Sum('rebote_ofensivo',output_field=FloatField()))) / Count("pk",output_field=FloatField()))*100) / Count("pk",output_field=FloatField())),
                                                                                       tl_rate = (Sum('tiro_libre_intentado') / Sum('tiros_campo_intentados'))*100,
                                                                                       p2_rate = (Sum('tiros_2_intentados') / Sum('tiros_campo_intentados'))*100,
                                                                                       p3_rate = (Sum('tiros_3_intentados') / Sum('tiros_campo_intentados'))*100,                                                 
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
                                                                                            tiros_campo_convertidos     = Sum('tiros_campo_convertidos'),
                                                                                            p_tiros_campo_convertidos   = Avg('tiros_campo_convertidos'),                                           
                                                                                            tiros_campo_intentados      = Sum('tiros_campo_intentados'),
                                                                                            p_tiros_campo_intentados    = Avg('tiros_campo_intentados'),
                                                                                            tiros_campo_porcentaje      = Case(
                                                                                                                         When(tiros_campo_intentados = 0, then = 0),
                                                                                                                         default = Sum('tiros_campo_convertidos') * 100/Sum('tiros_campo_intentados')),
                                                                                            tiros_2_convertidos         = Sum('tiros_2_convertidos'),
                                                                                            p_tiros_2_convertidos       = Avg('tiros_2_convertidos'),  
                                                                                            tiros_2_intentados          = Sum('tiros_2_intentados'),
                                                                                            p_tiros_2_intentados        = Avg('tiros_2_intentados'),
                                                                                            tiros_2_porcentaje          = Case(
                                                                                                                         When(tiros_2_intentados = 0, then = 0),
                                                                                                                         default = Sum('tiros_2_convertidos') * 100/Sum('tiros_2_intentados')),
                                                                                            tiros_3_convertidos = Sum('tiros_3_convertidos'),
                                                                                            p_tiros_3_convertidos = Avg('tiros_3_convertidos'),
                                                                                            tiros_3_intentados = Sum('tiros_3_intentados'),
                                                                                            p_tiros_3_intentados = Avg('tiros_3_intentados'),
                                                                                            tiros_3_porcentaje = Case(
                                                                                                                    When(tiros_3_intentados=0, then = 0),
                                                                                                                    default = Sum('tiros_3_convertidos')* 100 /Sum('tiros_3_intentados')),
                                                                                            tiro_libre_convertido = Sum('tiro_libre_convertido'),
                                                                                            p_tiro_libre_convertido = Avg('tiro_libre_convertido'),
                                                                                            tiro_libre_intentado = Sum('tiro_libre_intentado'),
                                                                                            p_tiro_libre_intentado = Avg('tiro_libre_intentado'),
                                                                                            tiros_libre_porcentaje = Case(
                                                                                                                        When(tiro_libre_intentado = 0, then= 0),
                                                                                                                        default = Sum('tiro_libre_convertido')*100/Sum('tiro_libre_intentado')),
                                                                                            rebote_ofensivo = Sum('rebote_ofensivo'),
                                                                                            p_rebote_ofensivo = Avg('rebote_ofensivo'),
                                                                                            rebote_defensivo = Sum('rebote_defensivo'),
                                                                                            p_rebote_defensivo = Avg('rebote_defensivo'),                                                                
                                                                                            rebote_total = Sum('rebote_total'),
                                                                                            p_rebote_total = Avg('rebote_total'),
                                                                                            asistencias = Sum('asistencias'),
                                                                                            p_asistencias = Avg('asistencias'),
                                                                                            perdidas = Sum('perdidas'),
                                                                                            p_perdidas = Avg('perdidas'),
                                                                                            recuperos = Sum('recuperos'),
                                                                                            p_recuperos = Avg('recuperos'),
                                                                                            tapones = Sum('tapones'),
                                                                                            p_tapones = Avg('tapones'),
                                                                                            faltas_personales = Sum('faltas_personales'),
                                                                                            p_faltas_personales = Avg('faltas_personales'),                                                                
                                                                                            valoración = Sum('valoración'),
                                                                                            p_valoración = Avg('valoración'),
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
        contexto['playerstats']     = self.get_queryset()
        contexto['plantel']         = Jugadores.objects.filter(id_equipo = self.kwargs['ide'], estado = "A")
        contexto['partidos']        = Estadistica_Equipo_Partido.objects.filter(id_equipo = self.kwargs['ide'])
        contexto['player']          = Jugadores.objects.filter(id = self.kwargs['idp']).get()
        contexto['quinteto']        = Estadistica_Jugador_Partido.objects.filter(id_partido__estadistica_equipo_partido__id_equipo = self.kwargs['ide'],id_jugador__id_equipo = self.kwargs['ide'], inicial = 1).order_by('-id_partido__detalle_partido')[:5]
        contexto['partidosjugador'] = Estadistica_Jugador_Partido.objects.filter(id_jugador = self.kwargs['idp']).order_by('id_partido__detalle_partido')
        a = 0
        for partido in contexto['partidos']:
           contexto['partidos'][a].equiporival        = Estadistica_Equipo_Partido.objects.filter(id_partido = partido.id_partido).exclude(id_equipo = self.kwargs['ide']).get()
           a = a + 1
        b = 0
        for partido in contexto['partidosjugador']:
           contexto['partidosjugador'][b].equiporival = Estadistica_Equipo_Partido.objects.filter(id_partido = partido.id_partido).exclude(id_equipo = self.kwargs['ide']).get()
           b = b + 1
                  
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())

class ActualizarJugador(UpdateView):
    model = Jugadores
    form_class = DetalleJugadorForm
    template_name = 'tfb/md-jugador.html'
    
    def get_context_data(self,**kwargs):
        contexto = super().get_context_data(**kwargs)
        return contexto

    def get_success_url(self):
        return reverse_lazy('tfb:detalle_jugador',kwargs = {'pk': self.kwargs['pk']})

