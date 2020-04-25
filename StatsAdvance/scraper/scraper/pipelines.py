# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .items import PartidoItem, JugadorItem, StatsTeamItem, StatsPlayerItem
from apps.tfb.models import Equipos, Jugadores, Partidos, Estadistica_Jugador_Partido, Estadistica_Equipo_Partido
from TUBSClass import StatsAdvance
import datetime

class ScraperPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, PartidoItem):
            return self.handlePartido(item, spider)
        if isinstance(item, JugadorItem):
            return self.handleJugador(item, spider)
        if isinstance(item, StatsTeamItem):
            return self.handleStatsTeam(item, spider)
        if isinstance(item, StatsPlayerItem):
            return self.handleStatsPlayer(item, spider)

    def handleJugador(self,item,spider):
        equipo = Equipos.objects.get(nombre__exact = item['equipo'])
        j, created = Jugadores.objects.update_or_create(id_equipo = equipo, id_jugador = item['id_jugador'], defaults = {'id_equipo': equipo, 'id_jugador': item['id_jugador'],'nombre': item['nombre'] ,'urlIMG':item['urlIMG']})
        return item

    def handlePartido(self,item,spider):
        id_partido      = item['fibalink'].split('/')[5]
        detalle_partido = item['detalle_partido'].split(' ')[3]
        partido = Partidos.objects.create(id_partido = id_partido, detalle_partido = detalle_partido)
        return item
    
    def handleStatsTeam(self,item,spider):
        #Resultado
        ResA = 2
        ResB = 2
        if item['puntosA'] > item['puntosB']:
            ResA = 1
            ResB = 0
        
        if item['puntosB'] > item['puntosA']:
            ResB = 1
            ResA = 0
        
        #EquipoA
        paceA        = StatsAdvance.pace(self,tiroscampointentados= float(item['tciA']) ,perdidas= float(item['perA']), tiroslibresintentados=float(item['tliA']),reboff=float(item['roA']))
        paceB        = StatsAdvance.pace(self,tiroscampointentados= float(item['tciB']) ,perdidas= float(item['perB']), tiroslibresintentados=float(item['tliB']),reboff=float(item['roB']))
        ptsxpaceA    = StatsAdvance.ptspace(self,puntos=float(item['puntosA']),pace= paceA)
        efFGA        = StatsAdvance.efFG(self,doblesconvertidos=float(item['t2cA']),triplesconvertidos=float(item['t3cA']),tiroscampointentados=float(item['tciA']))
        tSA          = StatsAdvance.ts(self,puntos=float(item['puntosA']),tiroscampointentados=float(item['tciA']),tiroslibresintentados=float(item['tliA']))
        effOFA       = StatsAdvance.effOff(self,puntos=float(item['puntosA']),pace=paceA)
        effDEFA      = StatsAdvance.effDef(self,puntosrival=float(item['puntosB']),pace=paceB)
        tRoA         = StatsAdvance.tRO(self,rebof=float(item['roA']),rebdef=float(item['rdB']))
        tRdA         = StatsAdvance.tRD(self,rebdef=float(item['rdA']),reboff=item['roB'])
        tAsA         = StatsAdvance.tAS(self,asistencias=float(item['asisA']),pace=paceA)
        tAsPerA      = StatsAdvance.tASPER(self,asistencias=float(item['asisA']) ,perdidas=float(item['perA']))
        tRecA        = StatsAdvance.tREC(self,recuperos=float(item['recA']),pace= paceA)
        tPerA        = StatsAdvance.tPER(self,perdidas=float(item['perA']),pace= paceA)
        opTLA        = StatsAdvance.opTL(self,tiroslibresconvertidos=float(item['tlcA']) ,tiroscampointentados= float(item['tciA']))
        idA          = Equipos.objects.get(nombre__exact = item['equipoA'])         
        #EquipoB
        ptsxpaceB    = StatsAdvance.ptspace(self,puntos=float(item['puntosB']),pace= paceB)
        efFGB        = StatsAdvance.efFG(self,doblesconvertidos=float(item['t2cB']),triplesconvertidos=float(item['t3cA']),tiroscampointentados=float(item['tciB']))
        tSB          = StatsAdvance.ts(self,puntos=float(item['puntosB']),tiroscampointentados=float(item['tciB']),tiroslibresintentados=float(item['tliB']))
        effOFB       = StatsAdvance.effOff(self,puntos=float(item['puntosB']),pace=paceB)
        effDEFB      = StatsAdvance.effDef(self,puntosrival=float(item['puntosA']),pace=paceA)
        tRoB         = StatsAdvance.tRO(self,rebof=float(item['roB']),rebdef=float(item['rdA']))
        tRdB         = StatsAdvance.tRD(self,rebdef=float(item['rdB']),reboff=item['roA'])
        tAsB         = StatsAdvance.tAS(self,asistencias=float(item['asisB']),pace=paceB)
        tAsPerB      = StatsAdvance.tASPER(self,asistencias=float(item['asisB']) ,perdidas=float(item['perB']))
        tRecB        = StatsAdvance.tREC(self,recuperos=float(item['recB']),pace= paceB)
        tPerB        = StatsAdvance.tPER(self,perdidas=float(item['perB']),pace= paceB)
        opTLB        = StatsAdvance.opTL(self,tiroslibresconvertidos=float(item['tlcB']) ,tiroscampointentados= float(item['tciA']))
        idB          = Equipos.objects.get(nombre__exact = item['equipoA'])
        
        equipoA      = Estadistica_Equipo_Partido.objects.create(
                                                    id_partido              = item['id_partido'], 
                                                    id_equipo               = idA,
                                                    puntos                  = item['puntosA'],
                                                    tiros_campo_convertidos = item['tccA'],
                                                    tiros_campo_intentados  = item['tciA'],
                                                    tiros_campo_porcentaje  = item['tcpA'],
                                                    tiros_2_convertidos     = item['t2cA'],
                                                    tiros_2_intentados      = item['t2iA'],
                                                    tiros_2_porcentaje      = item['t2pA'],
                                                    tiros_3_convertidos     = item['t3cA'],
                                                    tiros_3_intentados      = item['t3iA'],
                                                    tiros_3_porcentaje      = item['t3pA'],
                                                    tiro_libre_convertido   = item['tlcA'],
                                                    tiro_libre_intentado    = item['tliA'],
                                                    tiros_libre_porcentaje  = item['tlpA'],
                                                    rebote_ofensivo         = item['roA'],
                                                    rebote_defensivo        = item['rdA'],
                                                    rebote_total            = item['rtA'],
                                                    asistencias             = item['asisA'],
                                                    perdidas                = item['perA'],
                                                    recuperos               = item['recA'],
                                                    tapones                 = item['tapA'],
                                                    faltas_personales       = item['fpA'],
                                                    valoración              = item['valA'],
                                                    pace                    = paceA,
                                                    ptspace                 = ptsxpaceA,
                                                    eficiencia_tiro_campo   = efFGA,
                                                    true_shooting           = tSA,
                                                    eficiencia_ofensiva     = effOFA,
                                                    eficiencia_defensiva    = effDEFA,
                                                    tasa_rebote_ofensivo    = tRoA,
                                                    tasa_rebote_defensivo   = tRdA,
                                                    tasa_recuperos          = tRecA,
                                                    tasa_asistencias        = tAsA,
                                                    tasa_as_per             = tAsPerA,
                                                    tasa_perdidas           = tPerA,
                                                    oportunidad_tiro_libre  = opTLA,
                                                    puntos_de_perdidas      = item['puntos_de_perdidasA'],
                                                    puntos_pintura          = item['puntos_pinturaA'],
                                                    puntos_contraataque     = item['puntos_contraataqueA'],
                                                    puntos_banca            = item['puntos_bancaA'],
                                                    puntos_ro               = item['puntos_roA'],
                                                    partido_ganado          = ResA,)

        equipoB      = Estadistica_Equipo_Partido.objects.create(
                                                    id_partido              = item['id_partido'], 
                                                    id_equipo               = idB,
                                                    puntos                  = item['puntosB'],
                                                    tiros_campo_convertidos = item['tccB'],
                                                    tiros_campo_intentados  = item['tciB'],
                                                    tiros_campo_porcentaje  = item['tcpB'],
                                                    tiros_2_convertidos     = item['t2cB'],
                                                    tiros_2_intentados      = item['t2iB'],
                                                    tiros_2_porcentaje      = item['t2pB'],
                                                    tiros_3_convertidos     = item['t3cB'],
                                                    tiros_3_intentados      = item['t3iB'],
                                                    tiros_3_porcentaje      = item['t3pB'],
                                                    tiro_libre_convertido   = item['tlcB'],
                                                    tiro_libre_intentado    = item['tliB'],
                                                    tiros_libre_porcentaje  = item['tlpB'],
                                                    rebote_ofensivo         = item['roB'],
                                                    rebote_defensivo        = item['rdB'],
                                                    rebote_total            = item['rtB'],
                                                    asistencias             = item['asisB'],
                                                    perdidas                = item['perB'],
                                                    recuperos               = item['recB'],
                                                    tapones                 = item['tapB'],
                                                    faltas_personales       = item['fpB'],
                                                    valoración              = item['valB'],
                                                    pace                    = paceB,
                                                    ptspace                 = ptsxpaceB,
                                                    eficiencia_tiro_campo   = efFGB,
                                                    true_shooting           = tSB,
                                                    eficiencia_ofensiva     = effOFB,
                                                    eficiencia_defensiva    = effDEFB,
                                                    tasa_rebote_ofensivo    = tRoB,
                                                    tasa_rebote_defensivo   = tRdB,
                                                    tasa_recuperos          = tRecB,
                                                    tasa_asistencias        = tAsB,
                                                    tasa_as_per             = tAsPerB,
                                                    tasa_perdidas           = tPerB,
                                                    oportunidad_tiro_libre  = opTLB,
                                                    puntos_de_perdidas      = item['puntos_de_perdidasB'],
                                                    puntos_pintura          = item['puntos_pinturaB'],
                                                    puntos_contraataque     = item['puntos_contraataqueB'],
                                                    puntos_banca            = item['puntos_bancaB'],
                                                    puntos_ro               = item['puntos_roB'],
                                                    partido_ganado          = ResB,)
        return item

    def handleStatsPlayer(self, item, spider):
        #Avanzada
        pace         = StatsAdvance.pace(self,tiroscampointentados= float(item['tiros_campo_intentados']) ,perdidas= float(item['perdidas']), tiroslibresintentados=float(item['tiro_libre_intentado']),reboff=float(item['rebote_ofensivo']))
        ptsxpace     = StatsAdvance.ptspace(self,puntos=float(item['puntos']),pace= pace)
        efFG         = StatsAdvance.efFG(self,doblesconvertidos=float(item['tiros_2_convertidos']),triplesconvertidos=float(item['tiros_3_convertidos']),tiroscampointentados=float(item['tiros_campo_intentados']))
        tS           = StatsAdvance.ts(self,puntos=float(item['puntos']),tiroscampointentados=float(item['tiros_campo_intentados']),tiroslibresintentados=float(item['tiro_libre_intentado']))
        effOF        = StatsAdvance.effOff(self,puntos=float(item['puntos']),pace=pace)
        tAs          = StatsAdvance.tAS(self,asistencias=float(item['asistencias']),pace=pace)
        tAsPer       = StatsAdvance.tASPER(self,asistencias=float(item['asistencias']) ,perdidas=float(item['perdidas']))
        tRec         = StatsAdvance.tREC(self,recuperos=float(item['recuperos']),pace= pace)
        tPer         = StatsAdvance.tPER(self,perdidas=float(item['perdidas']),pace= pace)
        opTL         = StatsAdvance.opTL(self,tiroslibresconvertidos=float(item['tiro_libre_convertido']) ,tiroscampointentados= float(item['tiros_campo_intentado']))
        id_equipo    = Equipos.objects.get(nombre__exact = item['equipo'])

        jugador = Estadistica_Jugador_Partido.objects.create(
            id_partido              = item['id_partido'],
            id_jugador              = Jugadores.objects.get(id_equipo = id_equipo, id_jugador = item['id_jugador']),
            puntos                  = item['puntos'],
            minutos                 = datetime.datetime.strptime(item['minutos'],'%M:%S').time(),        
            tiros_campo_convertidos = item['tiros_campo_convertidos'],
            tiros_campo_intentados  = item['tiros_campo_intentados'],
            tiros_campo_porcentaje  = item['tiros_campo_porcentaje'],
            tiros_2_convertidos     = item['tiros_2_convertidos'],
            tiros_2_intentados      = item['tiros_2_intentados'],
            tiros_2_porcentaje      = item['tiros_2_porcentaje'],
            tiros_3_convertidos     = item['tiros_3_convertidos'],
            tiros_3_intentados      = item['tiros_3_intentados'],
            tiros_3_porcentaje      = item['tiros_3_porcentaje'],
            tiro_libre_convertido   = item['tiro_libre_convertido'],
            tiro_libre_intentado    = item['tiro_libre_intentado'],
            tiros_libre_porcentaje  = item['tiros_libre_porcentaje'],
            rebote_ofensivo         = item['rebote_ofensivo'],
            rebote_defensivo        = item['rebote_defensivo'],
            rebote_total            = item['rebote_total'],
            asistencias             = item['asistencias'],
            perdidas                = item['perdidas'],
            recuperos               = item['recuperos'],
            tapones                 = item['tapones'],
            faltas_personales       = item['faltas_personales'],
            faltas_recibidas        = item['faltas_recibidas'],
            diferencia_puntos       = item['diferencia_puntos'],
            valoración              = item['valoración'],
            pace                    = pace,
            ptspos                  = ptsxpace,
            eficiencia_tiro_campo   = efFG,
            true_shooting           = tS,
            eficiencia_ofensiva     = effOF,
            tasa_asistencias        = tAs,
            tasa_perdidas           = tPer,
            tasa_as_per             = tAsPer,
            tasa_recuperos          = tRec,
            oportunidad_tiro_libre  = opTL,
            )
        return item