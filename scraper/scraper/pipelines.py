# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from .items import PartidoItem, EquipoItem, JugadorItem, StatsTeamItem, StatsPlayerItem
from apps.tfb.models import Equipos, Jugadores, Partidos, Estadistica_Jugador_Partido, Estadistica_Equipo_Partido
from TUBSClass import StatsAdvance
import datetime

class ScraperPipeline(object):
    
    def __init__(self, *args, **kwargs):
        super(ScraperPipeline, self).__init__(*args, **kwargs)
        self.errorplayer = []

    def close_spider(self,spider):
        print(self.errorplayer)

    def process_item(self, item, spider):
        if isinstance(item, PartidoItem):
            return self.handlePartido(item, spider)
        if isinstance(item, JugadorItem):
            return self.handleJugador(item, spider)
        if isinstance(item, EquipoItem):
            return self.handleEquipo(item, spider)
        if isinstance(item, StatsTeamItem):
            return self.handleStatsTeam(item, spider)
        if isinstance(item, StatsPlayerItem):
            return self.handleStatsPlayer(item, spider)
    
    def handlePartido(self,item,spider):
        id_partido      = item['id_partido'].pop()
        detalle_partido = item['detalle_partido'].pop().split(' ')[3]
        partido = Partidos.objects.create(id_partido = id_partido, detalle_partido = datetime.date(int(detalle_partido.split('/')[2]),int(detalle_partido.split('/')[1]),int(detalle_partido.split('/')[0])))
        return partido

    def handleEquipo(self,item,spider):
        nombre_largo = item['nombre_largo'].pop()
        nombre_corto = item['nombre_corto'].pop()
        urlLogo      = item['urlLogo'].pop()
        equipo, created = Equipos.objects.get_or_create(nombre_corto = nombre_corto, defaults = {'nombre_largo': nombre_largo, 'nombre_corto': nombre_corto, 'urlLogo': urlLogo})          
        return equipo

    def handleJugador(self,item,spider):
        equipo      = Equipos.objects.get(nombre_corto__exact = item['equipo'].pop())
        id_jugador  = item['id_jugador'].pop()
        nombre      = item['nombre'].pop()
        apellido    = item['apellido'].pop()
        urlIMG      = item['urlIMG'].pop()
        if urlIMG is "":
            jugador, created = Jugadores.objects.update_or_create(id_equipo = equipo, id_jugador = id_jugador, defaults = {'id_equipo': equipo, 'id_jugador': id_jugador, 'nombre': nombre,'apellido': apellido, 'urlIMG':urlIMG})    
        else:
            try:
                jugador = Jugadores.objects.get(urlIMG = urlIMG)
                jugador.id_equipo  = equipo
                jugador.id_jugador = id_jugador
                jugador.save()
            except Jugadores.DoesNotExist:
                jugador, created = Jugadores.objects.update_or_create(id_equipo = equipo, id_jugador = id_jugador, defaults = {'id_equipo': equipo, 'id_jugador': id_jugador, 'nombre': nombre,'apellido': apellido, 'urlIMG':urlIMG})          
        return jugador

    def handleStatsTeam(self,item,spider):
        #PARTIDO
        id_partido   = Partidos.objects.get(id_partido = item['id_partido'].pop())
        #EQUIPOS
        id_equipoA   = Equipos.objects.get(nombre_corto__exact = item['equipoA'].pop())       
        id_equipoB   = Equipos.objects.get(nombre_corto__exact = item['equipoB'].pop())
        #ESTADISTICAS
        puntosA = item['puntosA'].pop() 
        puntosB = item['puntosB'].pop()
        q1A     = item['q1A'].pop()
        q1B     = item['q1B'].pop()
        q2A     = item['q2A'].pop()
        q2B     = item['q2B'].pop()
        q3A     = item['q3A'].pop()
        q3B     = item['q3B'].pop()
        q4A     = item['q4A'].pop()
        q4B     = item['q4B'].pop()
        tccA    = item['tccA'].pop()
        tccB    = item['tccB'].pop()
        tciA    = item['tciA'].pop()
        tciB    = item['tciB'].pop()
        tcpA    = item['tcpA'].pop()
        tcpB    = item['tcpB'].pop()
        t2cA    = item['t2cA'].pop()
        t2cB    = item['t2cB'].pop()
        t2iA    = item['t2iA'].pop()
        t2iB    = item['t2iB'].pop()
        t2pA    = item['t2pA'].pop()
        t2pB    = item['t2pB'].pop()
        t3cA    = item['t3cA'].pop()
        t3cB    = item['t3cB'].pop()
        t3iA    = item['t3iA'].pop()
        t3iB    = item['t3iB'].pop()
        t3pA    = item['t3pA'].pop()
        t3pB    = item['t3pB'].pop()
        tlcA    = item['tlcA'].pop()
        tlcB    = item['tlcB'].pop()
        tliA    = item['tliA'].pop()
        tliB    = item['tliB'].pop()  
        tlpA    = item['tlpA'].pop()
        tlpB    = item['tlpB'].pop()
        roA     = item['roA'].pop()
        roB     = item['roB'].pop()
        rdA     = item['rdA'].pop()
        rdB     = item['rdB'].pop()
        rtA     = item['rtA'].pop()
        rtB     = item['rtB'].pop()
        asisA   = item['asisA'].pop()
        asisB   = item['asisB'].pop()
        perA    = item['perA'].pop()
        perB    = item['perB'].pop()
        recA    = item['recA'].pop()
        recB    = item['recB'].pop()
        tapA    = item['tapA'].pop()
        tapB    = item['tapB'].pop()
        fpA     = item['fpA'].pop()
        fpB     = item['fpB'].pop()
        valA    = item['valA'].pop()
        valB    = item['valB'].pop()
        ptssupA = item['puntos_bancaA'].pop()
        ptssupB = item['puntos_bancaB'].pop()
        ptspinA = item['puntos_pinturaA'].pop()
        ptspinB = item['puntos_pinturaB'].pop()
        ptsroA  = item['puntos_roA'].pop()
        ptsroB  = item['puntos_roB'].pop()
        ptsctaA = item['puntos_contraataqueA'].pop()
        ptsctaB = item['puntos_contraataqueB'].pop()
        ptsperA = item['puntos_de_perdidasA'].pop()
        ptsperB = item['puntos_de_perdidasB'].pop()
        #RESULTADO
        ResA = 2
        ResB = 2
        if  puntosA > puntosB :
            ResA = 1
            ResB = 0
        
        if puntosB > puntosA:
            ResB = 1
            ResA = 0
        #ESTADISTICAS AVANZADAS
        #PACE
        paceA               = StatsAdvance.pace(self,tiroscampointentados= float(tciA) ,perdidas= float(perA), tiroslibresintentados=float(tliA),reboff=float(roA))
        paceB               = StatsAdvance.pace(self,tiroscampointentados= float(tciB) ,perdidas= float(perB), tiroslibresintentados=float(tliB),reboff=float(roB))
        #PTSPACE
        ptsxpaceA           = StatsAdvance.ptspace(self,puntos=float(puntosA),pace=paceA)
        ptsxpaceB           = StatsAdvance.ptspace(self,puntos=float(puntosB),pace=paceB)
        #EFICIENCIA DE TIRO
        efFGA               = StatsAdvance.efFG(self,doblesconvertidos=float(t2cA),triplesconvertidos=float(t3cA),tiroscampointentados=float(tciA))
        efFGB               = StatsAdvance.efFG(self,doblesconvertidos=float(t2cB),triplesconvertidos=float(t3cB),tiroscampointentados=float(tciB))
        #TRUE SHOOTING
        tSA                 = StatsAdvance.ts(self,puntos=float(puntosA),tiroscampointentados=float(tciA),tiroslibresintentados=float(tliA))
        tSB                 = StatsAdvance.ts(self,puntos=float(puntosB),tiroscampointentados=float(tciB),tiroslibresintentados=float(tliB))
        #EFICIENCIA OFENSIVA
        effOFA              = StatsAdvance.effOff(self,puntos=float(puntosA),pace=paceA)
        effOFB              = StatsAdvance.effOff(self,puntos=float(puntosB),pace=paceB)
        #EFICIENCIA DEFENSIVA
        effDEFA             = StatsAdvance.effDef(self,puntosrival=float(puntosB),pace=paceB)
        effDEFB             = StatsAdvance.effDef(self,puntosrival=float(puntosA),pace=paceA)
        #RATIO REBOTE OFENSIVO
        tRoA                = StatsAdvance.tRO(self,rebof=float(roA),rebdef=float(rdB))
        tRoB                = StatsAdvance.tRO(self,rebof=float(roB),rebdef=float(rdA))
        #RATIO REBOTE DEFENSIVO
        tRdA                = StatsAdvance.tRD(self,rebdef=float(rdA),reboff=roB)
        tRdB                = StatsAdvance.tRD(self,rebdef=float(rdB),reboff=roA)
        #PORCENTAJE ASISTENCIAS POR POSESION
        tAsA                = StatsAdvance.tAS(self,asistencias=float(asisA),pace=paceA)
        tAsB                = StatsAdvance.tAS(self,asistencias=float(asisB),pace=paceB)
        #PORCENTAJE TIRO CAMPO ASISTIDOS
        tcasA               = StatsAdvance.tTCAS(self,tiroscampoconvertidos=tccA,asistencias=asisA)
        tcasB               = StatsAdvance.tTCAS(self,tiroscampoconvertidos=tccB,asistencias=asisB)
        #PORCENTAJE ASISTENCIAS POR PERDIDA
        tAsPerA             = StatsAdvance.tASPER(self,asistencias=float(asisA) ,perdidas=float(perA))
        tAsPerB             = StatsAdvance.tASPER(self,asistencias=float(asisB) ,perdidas=float(perB))
        #PORCENTAJE RECUPEROS POR POSESION
        tRecA               = StatsAdvance.tREC(self,recuperos=float(recA),pace= paceA)
        tRecB               = StatsAdvance.tREC(self,recuperos=float(recB),pace= paceB)
        #PORCENTAJE PERDIDAS POR POSESION
        tPerA               = StatsAdvance.tPER(self,perdidas=float(perA),pace= paceA)
        tPerB               = StatsAdvance.tPER(self,perdidas=float(perB),pace= paceB)
        #PORCENTAJE PERDIDAS POR POSESION
        tTapA               = StatsAdvance.tTAP(self,tapones=float(tapA),pace= paceA)
        tTapB               = StatsAdvance.tTAP(self,tapones=float(tapB),pace= paceB)
        #VOLUMEN TIROS LIBRES SOBRE TIRO CAMPO
        vTLA                = StatsAdvance.VTLTC(self,tiroslibresintentados=float(tliA) ,tiroscampointentados= float(tciA))
        vTLB                = StatsAdvance.VTLTC(self,tiroslibresintentados=float(tliB) ,tiroscampointentados= float(tciB))
        #VOLUMEN TIROS DE 2 SOBRE TIRO CAMPO
        v2PA                = StatsAdvance.V2PTC(self,doblesintentados=float(t2iA) ,tiroscampointentados= float(tciA))
        v2PB                = StatsAdvance.V2PTC(self,doblesintentados=float(t2iB) ,tiroscampointentados= float(tciB))
        #VOLUMEN TIROS DE 3 SOBRE TIRO CAMPO
        v3PA                = StatsAdvance.V3PTC(self,triplesintentados=float(t3iA) ,tiroscampointentados= float(tciA))
        v3PB                = StatsAdvance.V3PTC(self,triplesintentados=float(t3iB) ,tiroscampointentados= float(tciB))
        
        equipoA             = Estadistica_Equipo_Partido.objects.create(
                                                    id_partido              = id_partido, 
                                                    id_equipo               = id_equipoA,
                                                    localia                 = 1,
                                                    puntos                  = puntosA,
                                                    q1                      = q1A,
                                                    q2                      = q2A,
                                                    q3                      = q3A,
                                                    q4                      = q4A,                
                                                    tiros_campo_convertidos = tccA,
                                                    tiros_campo_intentados  = tciA,
                                                    tiros_campo_porcentaje  = tcpA,
                                                    tiros_2_convertidos     = t2cA,
                                                    tiros_2_intentados      = t2iA,
                                                    tiros_2_porcentaje      = t2pA,
                                                    tiros_3_convertidos     = t3cA,
                                                    tiros_3_intentados      = t3iA,
                                                    tiros_3_porcentaje      = t3pA,
                                                    tiro_libre_convertido   = tlcA,
                                                    tiro_libre_intentado    = tliA,
                                                    tiros_libre_porcentaje  = tlpA,
                                                    rebote_ofensivo         = roA,
                                                    rebote_defensivo        = rdA,
                                                    rebote_total            = rtA,
                                                    asistencias             = asisA,
                                                    perdidas                = perA,
                                                    recuperos               = recA,
                                                    tapones                 = tapA,
                                                    faltas_personales       = fpA,
                                                    valoración              = valA,
                                                    pace                    = paceA,
                                                    ptsxpace                = ptsxpaceA,
                                                    eficiencia_tiro_campo   = efFGA,
                                                    true_shooting           = tSA,
                                                    tiros_campo_asistidos   = tcasA,
                                                    eficiencia_ofensiva     = effOFA,
                                                    eficiencia_defensiva    = effDEFA,
                                                    tasa_rebote_ofensivo    = tRoA,
                                                    tasa_rebote_defensivo   = tRdA,
                                                    tasa_recuperos          = tRecA,
                                                    tasa_tapones            = tTapA,
                                                    tasa_asistencias        = tAsA,
                                                    tasa_as_per             = tAsPerA,
                                                    tasa_perdidas           = tPerA,
                                                    tl_rate                 = vTLA,
                                                    p2_rate                 = v2PA,
                                                    p3_rate                 = v3PA,
                                                    puntos_de_perdidas      = ptsperA,
                                                    puntos_pintura          = ptspinA,
                                                    puntos_contraataque     = ptsctaA,
                                                    puntos_banca            = ptssupA,
                                                    puntos_ro               = ptsroA,
                                                    partido_ganado          = ResA,)

        equipoB             = Estadistica_Equipo_Partido.objects.create(
                                                    id_partido              = id_partido, 
                                                    id_equipo               = id_equipoB,
                                                    localia                 = 0,
                                                    puntos                  = puntosB,
                                                    q1                      = q1B,
                                                    q2                      = q2B,
                                                    q3                      = q3B,
                                                    q4                      = q4B,
                                                    tiros_campo_convertidos = tccB,
                                                    tiros_campo_intentados  = tciB,
                                                    tiros_campo_porcentaje  = tcpB,
                                                    tiros_2_convertidos     = t2cB,
                                                    tiros_2_intentados      = t2iB,
                                                    tiros_2_porcentaje      = t2pB,
                                                    tiros_3_convertidos     = t3cB,
                                                    tiros_3_intentados      = t3iB,
                                                    tiros_3_porcentaje      = t3pB,
                                                    tiro_libre_convertido   = tlcB,
                                                    tiro_libre_intentado    = tliB,
                                                    tiros_libre_porcentaje  = tlpB,
                                                    rebote_ofensivo         = roB,
                                                    rebote_defensivo        = rdB,
                                                    rebote_total            = rtB,
                                                    asistencias             = asisB,
                                                    perdidas                = perB,
                                                    recuperos               = recB,
                                                    tapones                 = tapB,
                                                    faltas_personales       = fpB,
                                                    valoración              = valB,
                                                    pace                    = paceB,
                                                    ptsxpace                 = ptsxpaceB,
                                                    eficiencia_tiro_campo   = efFGB,
                                                    true_shooting           = tSB,
                                                    tiros_campo_asistidos   = tcasB,
                                                    eficiencia_ofensiva     = effOFB,
                                                    eficiencia_defensiva    = effDEFB,
                                                    tasa_rebote_ofensivo    = tRoB,
                                                    tasa_rebote_defensivo   = tRdB,
                                                    tasa_recuperos          = tRecB,
                                                    tasa_tapones            = tTapB,
                                                    tasa_asistencias        = tAsB,
                                                    tasa_as_per             = tAsPerB,
                                                    tasa_perdidas           = tPerB,
                                                    tl_rate                 = vTLB,
                                                    p2_rate                 = v2PB,
                                                    p3_rate                 = v3PB,
                                                    puntos_de_perdidas      = ptsperB,
                                                    puntos_pintura          = ptspinB,
                                                    puntos_contraataque     = ptsctaB,
                                                    puntos_banca            = ptssupB,
                                                    puntos_ro               = ptsroB,
                                                    partido_ganado          = ResB,)
        
        return item

    def handleStatsPlayer(self, item, spider):
        #PARTIDO
        id_partido   = Partidos.objects.get(id_partido = item['id_partido'].pop())
        #INFO JUGADOR
        idequipo = item['equipo'].pop()
        idjug = item['id_jugador'].pop()
        try:
            id_equipo    = Equipos.objects.get(nombre_corto__exact = idequipo)
        except Equipos.DoesNotExist:    
            raise DropItem(item)
            self.errorplayer.append(str('el equipo' + idequipo +'no existe'+ id_partido)) 
            raise
        try:         
            id_jugador   = Jugadores.objects.get(id_equipo = id_equipo, id_jugador = idjug)
        except Jugadores.DoesNotExist:
            raise DropItem(item)
            self.errorplayer.append(str(idjug + '-' + idequipo + '-' + id_partido))
        #ESTADISTICAS
        puntos  = item['puntos'].pop() 
        minutos = item['minutos'].pop()
        tcc     = item['tiros_campo_convertidos'].pop()
        tci     = item['tiros_campo_intentados'].pop()
        tcp     = item['tiros_campo_porcentaje'].pop()
        t2c     = item['tiros_2_convertidos'].pop()
        t2i     = item['tiros_2_intentados'].pop()
        t2p     = item['tiros_2_porcentaje'].pop()
        t3c     = item['tiros_3_convertidos'].pop()
        t3i     = item['tiros_3_intentados'].pop()
        t3p     = item['tiros_3_porcentaje'].pop()
        tlc     = item['tiro_libre_convertido'].pop()
        tli     = item['tiro_libre_intentado'].pop()  
        tlp     = item['tiros_libre_porcentaje'].pop()
        ro      = item['rebote_ofensivo'].pop()
        rd      = item['rebote_defensivo'].pop()
        rt      = item['rebote_total'].pop()
        asis    = item['asistencias'].pop()
        per     = item['perdidas'].pop()
        rec     = item['recuperos'].pop()
        tap     = item['tapones'].pop()
        fp      = item['faltas_personales'].pop()
        fr      = item['faltas_recibidas'].pop()
        difpt   = item['diferencia_puntos'].pop()
        val     = item['valoración'].pop()
        #ESTADISTICAS AVANZADAS
        #PACE
        pace                = StatsAdvance.pace(self,tiroscampointentados= float(tci) ,perdidas= float(per), tiroslibresintentados=float(tli),reboff=float(ro))
        #PTSPACE
        ptsxpace            = StatsAdvance.ptspace(self,puntos=float(puntos),pace=pace)
        #EFICIENCIA DE TIRO
        efFG                = StatsAdvance.efFG(self,doblesconvertidos=float(t2c),triplesconvertidos=float(t3c),tiroscampointentados=float(tci))
        #TRUE SHOOTING
        tS                  = StatsAdvance.ts(self,puntos=float(puntos),tiroscampointentados=float(tci),tiroslibresintentados=float(tli))
        #EFICIENCIA OFENSIVA
        effOF               = StatsAdvance.effOff(self,puntos=float(puntos),pace=pace)
        #PORCENTAJE ASISTENCIAS POR POSESION
        tAs                 = StatsAdvance.tAS(self,asistencias=float(asis),pace=pace)
        #PORCENTAJE ASISTENCIAS POR PERDIDA
        tAsPer              = StatsAdvance.tASPER(self,asistencias=float(asis) ,perdidas=float(per))
        #PORCENTAJE RECUPEROS POR POSESION
        tRec                = StatsAdvance.tREC(self,recuperos=float(rec),pace= pace)
        #PORCENTAJE PERDIDAS POR POSESION
        tPer                = StatsAdvance.tPER(self,perdidas=float(per),pace= pace)
        #PORCENTAJE TAPAS POR POSESION
        tTap                = StatsAdvance.tTAP(self,tapones=float(tap),pace= pace)
        #VOLUMEN TIROS LIBRES SOBRE TIRO CAMPO
        vTL                 = StatsAdvance.VTLTC(self,tiroslibresintentados=float(tli) ,tiroscampointentados= float(tci))
        #VOLUMEN TIROS DE 2 SOBRE TIRO CAMPO
        v2P                 = StatsAdvance.V2PTC(self,doblesintentados=float(t2i) ,tiroscampointentados= float(tci))
        #VOLUMEN TIROS DE 3 SOBRE TIRO CAMPO
        v3P                 = StatsAdvance.V3PTC(self,triplesintentados=float(t3i) ,tiroscampointentados= float(tci))
        #USO OFENSIVO
        usg                 = StatsAdvance.USG(self,tiroslibresintentados=tli,tiroscampointentados=tci,perdidas=per,pace=pace)
        
        jugador             = Estadistica_Jugador_Partido.objects.create(
            id_partido              = id_partido,
            id_jugador              = id_jugador,
            puntos                  = puntos,
            minutos                 = datetime.datetime.strptime(minutos,'%M:%S').time(),        
            tiros_campo_convertidos = tcc,
            tiros_campo_intentados  = tci,
            tiros_campo_porcentaje  = tcp,
            tiros_2_convertidos     = t2c,
            tiros_2_intentados      = t2i,
            tiros_2_porcentaje      = t2p,
            tiros_3_convertidos     = t3c,
            tiros_3_intentados      = t3i,
            tiros_3_porcentaje      = t3p,
            tiro_libre_convertido   = tlc,
            tiro_libre_intentado    = tli,
            tiros_libre_porcentaje  = tlp,
            rebote_ofensivo         = ro,
            rebote_defensivo        = rd,
            rebote_total            = rt,
            asistencias             = asis,
            perdidas                = per,
            recuperos               = rec,
            tapones                 = tap,
            faltas_personales       = fp,
            faltas_recibidas        = fr,
            diferencia_puntos       = difpt,
            valoración              = val,
            pace                    = pace,
            ptspace                 = ptsxpace,
            eficiencia_tiro_campo   = efFG,
            true_shooting           = tS,
            eficiencia_ofensiva     = effOF,
            tasa_tapones            = tTap,
            tasa_asistencias        = tAs,
            tasa_perdidas           = tPer,
            tasa_as_per             = tAsPer,
            tasa_recuperos          = tRec,
            tl_rate                 = vTL,
            p2_rate                 = v2P,
            p3_rate                 = v3P,
            usg                     = usg,
            )
        
        return item

