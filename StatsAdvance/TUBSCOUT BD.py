import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StatsAdvance.settings.local")
import django
from selenium import webdriver 
import pandas as pd
import chromedriver_binary
from bs4 import BeautifulSoup
import datetime
from TUBSClass import StatsAdvance


django.setup()

from apps.tfb.models import Equipos, Jugadores, Partidos, Estadistica_Jugador_Partido, Estadistica_Equipo_Partido


options = webdriver.ChromeOptions()
options.add_argument('headless')

browser = webdriver.Chrome(options=options)
url = input('Ingrese el link del partido: ')
browser.get(url)


soup = BeautifulSoup(browser.page_source, "lxml")

partido = Partidos()

equipoA = Equipos.objects.get(nombre__exact = soup.find('span', id = 'aj_1_name').getText())
equipoB = Equipos.objects.get(nombre__exact = soup.find('span', id = 'aj_2_name').getText())

partido.id_partido = soup.find('input', id = 'matchId').get('value')
partido.save()

# INSERT ESTADISTICAS JUGADORES

a= 0
b= 0


for jugadorA in soup.find_all('a', attrs = {'tno':'1'}):
    if jugadorA.get('pno') is '0':
        print(equipoA)
    else:
        puntos                 = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sPoints').getText()
        tiros_campo_intentados = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sFieldGoalsAttempted').getText()
        tiros_2_convertidos    = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sTwoPointersMade').getText()
        tiros_3_convertidos    = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sThreePointersMade').getText()
        tiro_libre_convertido  = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sFreeThrowsMade').getText()
        tiro_libre_intentado   = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sFreeThrowsAttempted').getText()
        ro                     = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sReboundsOffensive').getText()
        perdidas               = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sTurnovers').getText()
        asistencias            = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sAssists').getText()
        recuperos              = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sSteals').getText()
        
        pace = StatsAdvance.pace(self,tiroscampointentados=tiros_campo_intentados,perdidas=perdidas,tiroslibresintentados=tiro_libre_intentado,reboff=ro)
    
        jugador = Estadistica_Jugador_Partido.objects.create(
            id_partido = partido,
            id_jugador = Jugadores.objects.get(id_equipo = equipoA , id_jugador = jugadorA.get('pno')), 
            puntos = puntos,
            minutos = datetime.datetime.strptime(soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sMinutes').getText(),'%M:%S').time(),        
            tiros_campo_convertidos = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sFieldGoalsMade').getText(),
            tiros_campo_intentados = tiros_campo_intentados,
            tiros_campo_porcentaje = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sFieldGoalsPercentage').getText(),
            tiros_2_convertidos = tiros_2_convertidos,
            tiros_2_intentados = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sTwoPointersAttempted').getText(),
            tiros_2_porcentaje = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sTwoPointersPercentage').getText(),
            tiros_3_convertidos = tiros_3_convertidos,
            tiros_3_intentados = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sThreePointersAttempted').getText(),
            tiros_3_porcentaje = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sThreePointersPercentage').getText(),
            tiro_libre_convertido = tiro_libre_convertido,
            tiro_libre_intentado = tiro_libre_intentado,
            tiros_libre_porcentaje = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sFreeThrowsPercentage').getText(),
            rebote_ofensivo = ro,
            rebote_defensivo = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sReboundsDefensive').getText(),
            rebote_total = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sReboundsTotal').getText(),
            asistencias = asistencias,
            perdidas = perdidas,
            recuperos = recuperos,
            tapones = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sBlocks').getText(),
            faltas_personales = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sFoulsPersonal').getText(),
            diferencia_puntos = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_sPlusMinusPoints').getText(),
            valoración = soup.find('span', id = 'aj_1_'+jugadorA.get('pno')+'_eff_1').getText(),
            pace   = pace,
            ptspos = StatsAdvance.ptspace(self,puntos=float(puntos),pace=pace),
            efFG   = StatsAdvance.efFG(self,doblesconvertidos=float(tiros_2_convertidos),triplesconvertidos=float(tiros_3_convertidos),tiroscampointentados=float(tiros_campo_intentados)),
            ts     = StatsAdvance.ts(self,puntos=float(puntos),tiroscampointentados=float(tiros_campo_intentados),tiroslibresintentados=float(tiro_libre_intentado)),
            asper  = StatsAdvance.tASPER(self,asistencias=float(asistencias),perdidas=float(perdidas)),
            tas    = StatsAdvance.tAS(self,asistencias=float(asistencias),pace=pace),
            tper   = StatsAdvance.tPER(self,perdidas=float(perdidas),pace=pace),
            trec   = StatsAdvance.tREC(self,recuperos=float(recuperos),pace=pace),
            opTL   = StatsAdvance.opTL(self,tiroslibresconvertidos=float(tiro_libre_convertido),tiroscampointentados=float(tiros_campo_intentados)),
        )
        a = a + 1
        print(a)

for jugadorB in soup.find_all('a', attrs = {'tno':'2'}):   
    if jugadorB.get('pno') is '0':
        print(equipoB)
    else:    
        puntos                 = soup.find('span', id = 'aj_2_'+jugadorA.get('pno')+'_sPoints').getText()
        tiros_campo_intentados = soup.find('span', id = 'aj_2_'+jugadorA.get('pno')+'_sFieldGoalsAttempted').getText()
        tiros_2_convertidos    = soup.find('span', id = 'aj_2_'+jugadorA.get('pno')+'_sTwoPointersMade').getText()
        tiros_3_convertidos    = soup.find('span', id = 'aj_2_'+jugadorA.get('pno')+'_sThreePointersMade').getText()
        tiro_libre_convertido  = soup.find('span', id = 'aj_2_'+jugadorA.get('pno')+'_sFreeThrowsMade').getText()
        tiro_libre_intentado   = soup.find('span', id = 'aj_2_'+jugadorA.get('pno')+'_sFreeThrowsAttempted').getText()
        ro                     = soup.find('span', id = 'aj_2_'+jugadorA.get('pno')+'_sReboundsOffensive').getText()
        perdidas               = soup.find('span', id = 'aj_2_'+jugadorA.get('pno')+'_sTurnovers').getText()
        asistencias            = soup.find('span', id = 'aj_2_'+jugadorA.get('pno')+'_sAssists').getText()
        recuperos              = soup.find('span', id = 'aj_2_'+jugadorA.get('pno')+'_sSteals').getText()
        
        pace = StatsAdvance.pace(self,tiroscampointentados=tiros_campo_intentados,perdidas=perdidas,tiroslibresintentados=tiro_libre_intentado,reboff=ro)
    
        
        jugador = Estadistica_Jugador_Partido.objects.create(
            id_partido = partido,
            id_jugador = Jugadores.objects.get(id_equipo = equipoB, id_jugador = jugadorB.get('pno')),
            puntos = puntos,
            minutos = datetime.datetime.strptime(soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sMinutes').getText(),'%M:%S').time(),        
            tiros_campo_convertidos = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sFieldGoalsMade').getText(),
            tiros_campo_intentados = tiros_campo_intentados,
            tiros_campo_porcentaje = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sFieldGoalsPercentage').getText(),
            tiros_2_convertidos = tiros_2_convertidos,
            tiros_2_intentados = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sTwoPointersAttempted').getText(),
            tiros_2_porcentaje = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sTwoPointersPercentage').getText(),
            tiros_3_convertidos = tiros_3_convertidos,
            tiros_3_intentados = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sThreePointersAttempted').getText(),
            tiros_3_porcentaje = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sThreePointersPercentage').getText(),
            tiro_libre_convertido = tiro_libre_convertido,
            tiro_libre_intentado = tiro_libre_intentado,
            tiros_libre_porcentaje = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sFreeThrowsPercentage').getText(),
            rebote_ofensivo = ro,
            rebote_defensivo = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sReboundsDefensive').getText(),
            rebote_total = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sReboundsTotal').getText(),
            asistencias = asistencias,
            perdidas = perdidas,
            recuperos = recuperos,
            tapones = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sBlocks').getText(),
            faltas_personales = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sFoulsPersonal').getText(),
            diferencia_puntos = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_sPlusMinusPoints').getText(),
            valoración = soup.find('span', id = 'aj_2_'+jugadorB.get('pno')+'_eff_1').getText(),
            pace   = pace,
            ptspos = StatsAdvance.ptspace(self,puntos=float(puntos),pace=pace),
            efFG   = StatsAdvance.efFG(self,doblesconvertidos=float(tiros_2_convertidos),triplesconvertidos=float(tiros_3_convertidos),tiroscampointentados=float(tiros_campo_intentados)),
            ts     = StatsAdvance.ts(self,puntos=float(puntos),tiroscampointentados=float(tiros_campo_intentados),tiroslibresintentados=float(tiro_libre_intentado)),
            asper  = StatsAdvance.tASPER(self,asistencias=float(asistencias),perdidas=float(perdidas)),
            tas    = StatsAdvance.tAS(self,asistencias=float(asistencias),pace=pace),
            tper   = StatsAdvance.tPER(self,perdidas=float(perdidas),pace=pace),
            trec   = StatsAdvance.tREC(self,recuperos=float(recuperos),pace=pace),
            opTL   = StatsAdvance.opTL(self,tiroslibresconvertidos=float(tiro_libre_convertido),tiroscampointentados=float(tiros_campo_intentados)),
            )
        b = b + 1
        print(b)

# INSERT ESTADISTICA DE EQUIPO
puntosL = soup.find('span',attrs={'id':'aj_1_tot_sPoints'}).getText()
tccL = soup.find('span',attrs={'id':'aj_1_tot_sFieldGoalsMade'}).getText()
tciL = soup.find('span',attrs={'id':'aj_1_tot_sFieldGoalsAttempted'}).getText()
tcpL = soup.find('span',attrs={'id':'aj_1_tot_sFieldGoalsPercentage'}).getText()
p2cL = soup.find('span',attrs={'id':'aj_1_tot_sTwoPointersMade'}).getText()
p2iL = soup.find('span',attrs={'id':'aj_1_tot_sTwoPointersAttempted'}).getText()
p2pL = soup.find('span',attrs={'id':'aj_1_tot_sTwoPointersPercentage'}).getText()
p3cL = soup.find('span',attrs={'id':'aj_1_tot_sThreePointersMade'}).getText()
p3iL = soup.find('span',attrs={'id':'aj_1_tot_sThreePointersAttempted'}).getText()
p3pL = soup.find('span',attrs={'id':'aj_1_tot_sThreePointersPercentage'}).getText()
tlcL = soup.find('span',attrs={'id':'aj_1_tot_sFreeThrowsMade'}).getText()
tliL = soup.find('span',attrs={'id':'aj_1_tot_sFreeThrowsAttempted'}).getText()
tlpL = soup.find('span',attrs={'id':'aj_1_tot_sFreeThrowsPercentage'}).getText()
roL = soup.find('span',attrs={'id':'aj_1_tot_sReboundsOffensive'}).getText()
rdL = soup.find('span',attrs={'id':'aj_1_tot_sReboundsDefensive'}).getText()
rtL = soup.find('span',attrs={'id':'aj_1_tot_sReboundsTotal'}).getText()
asistL = soup.find('span',attrs={'id':'aj_1_tot_sAssists'}).getText()
perL = soup.find('span',attrs={'id':'aj_1_tot_sTurnovers'}).getText()
recL = soup.find('span',attrs={'id':'aj_1_tot_sSteals'}).getText()
tapL = soup.find('span',attrs={'id':'aj_1_tot_sBlocks'}).getText()
fpL = soup.find('span',attrs={'id':'aj_1_tot_sFoulsTotal'}).getText()
valL = soup.find('span',attrs={'id':'aj_1_tot_eff_1'}).getText()
ptsPerdidasA = soup.find('span',attrs={'id':'aj_1_tot_sPointsFromTurnovers'}).getText()
ptsPinturaA = soup.find('span',attrs={'id':'aj_1_tot_sPointsInThePaint'}).getText()
ptsSegundaChanceA = soup.find('span',attrs={'id':'aj_1_tot_sPointsSecondChance'}).getText()
ptsContraataqueA = soup.find('span',attrs={'id':'aj_1_tot_sPointsFastBreak'}).getText()
ptsBancaA = soup.find('span',attrs={'id':'aj_1_tot_sBenchPoints'}).getText()

puntosV = soup.find('span',attrs={'id':'aj_2_tot_sPoints'}).getText()
tccV = soup.find('span',attrs={'id':'aj_2_tot_sFieldGoalsMade'}).getText()
tciV = soup.find('span',attrs={'id':'aj_2_tot_sFieldGoalsAttempted'}).getText()
tcpV = soup.find('span',attrs={'id':'aj_2_tot_sFieldGoalsPercentage'}).getText()
p2cV = soup.find('span',attrs={'id':'aj_2_tot_sTwoPointersMade'}).getText()
p2iV = soup.find('span',attrs={'id':'aj_2_tot_sTwoPointersAttempted'}).getText()
p2pV = soup.find('span',attrs={'id':'aj_2_tot_sTwoPointersPercentage'}).getText()
p3cV = soup.find('span',attrs={'id':'aj_2_tot_sThreePointersMade'}).getText()
p3iV = soup.find('span',attrs={'id':'aj_2_tot_sThreePointersAttempted'}).getText()
p3pV = soup.find('span',attrs={'id':'aj_2_tot_sThreePointersPercentage'}).getText()
tlcV = soup.find('span',attrs={'id':'aj_2_tot_sFreeThrowsMade'}).getText()
tliV = soup.find('span',attrs={'id':'aj_2_tot_sFreeThrowsAttempted'}).getText()
tlpV = soup.find('span',attrs={'id':'aj_2_tot_sFreeThrowsPercentage'}).getText()
roV = soup.find('span',attrs={'id':'aj_2_tot_sReboundsOffensive'}).getText()
rdV = soup.find('span',attrs={'id':'aj_2_tot_sReboundsDefensive'}).getText()
rtV = soup.find('span',attrs={'id':'aj_2_tot_sReboundsTotal'}).getText()
asistV = soup.find('span',attrs={'id':'aj_2_tot_sAssists'}).getText()
perV = soup.find('span',attrs={'id':'aj_2_tot_sTurnovers'}).getText()
recV = soup.find('span',attrs={'id':'aj_2_tot_sSteals'}).getText()
tapV = soup.find('span',attrs={'id':'aj_2_tot_sBlocks'}).getText()
fpV = soup.find('span',attrs={'id':'aj_2_tot_sFoulsTotal'}).getText()
valV = soup.find('span',attrs={'id':'aj_2_tot_eff_1'}).getText()
ptsPerdidasB = soup.find('span',attrs={'id':'aj_2_tot_sPointsFromTurnovers'}).getText()
ptsPinturaB = soup.find('span',attrs={'id':'aj_2_tot_sPointsInThePaint'}).getText()
ptsSegundaChanceB = soup.find('span',attrs={'id':'aj_2_tot_sPointsSecondChance'}).getText()
ptsContraataqueB = soup.find('span',attrs={'id':'aj_2_tot_sPointsFastBreak'}).getText()
ptsBancaB = soup.find('span',attrs={'id':'aj_2_tot_sBenchPoints'}).getText()

#ESTADISTICAS AVANZADAS

#Posesiones
paceL = StatsAdvance.pace(self,tiroscampointentados=float(tciL),perdidas=float(perL),tiroslibresintentados=float(tliL),reboff=float(roL))
paceV = StatsAdvance.pace(self,tiroscampointentados=float(tciV),perdidas=float(perV),tiroslibresintentados=float(tliV),reboff=float(roV))

#PTSXPACE
ptspaceL = StatsAdvance.ptspace(self,puntos=float(puntosL),pace=(paceL))
ptspaceL = StatsAdvance.ptspace(self,puntos=float(puntosV),pace=(paceV))

#Eficiencia
efOfensivaL = StatsAdvance.effOff(self,puntos=float(puntosL),pace=paceL)
efOfensivaV = StatsAdvance.effOff(self,puntos=float(puntosV),pace=paceV) 
eFGL = StatsAdvance.efFG(self,doblesconvertidos=float(p2cL),triplesconvertidos=float(p3cL),tiroscampointentados=float(tciL))

efDefensivaL = efOfensivaV
efDefensivaV = efOfensivaL
eFGV = StatsAdvance.efFG(self,doblesconvertidos=float(p2cV),triplesconvertidos=float(p3cV),tiroscampointentados=float(tciV))

#Tiro Real
tiroRealL = StatsAdvance.ts(self,puntos=float(puntosL),tiroscampointentados=float(tciL),tiroslibresintentados=float(tliL))
tiroRealV = StatsAdvance.ts(self,puntos=float(puntosV),tiroscampointentados=float(tciV),tiroslibresintentados=float(tliV))
  
#Rebotes
tasaROL = StatsAdvance.tRO(self,rebof=float(roL),rebdef=float(rdV))
tasaRDL = StatsAdvance.tRD(self,rebdef=float(rdL),reboff=float(roV))

tasaROV = StatsAdvance.tRO(self,rebof=float(roV),rebdef=float(rdL))
tasaRDV = StatsAdvance.tRD(self,rebdef=float(rdV),reboff=float(roL))

#Asistencias
tasaAsisL = StatsAdvance.tAS(self,asistencias=float(asistL),pace=paceL)
tasaAsisV = StatsAdvance.tAS(self,asistencias=float(asistV),pace=paceV)

#AS/PER
asPerL= StatsAdvance.tASPER(self,asistencias=float(asistL),perdidas=float(perL))  
asPerV= StatsAdvance.tASPER(self,asistencias=float(asistV),perdidas=float(perV))

#Recuperos
tasaRecL = StatsAdvance.tREC(self,recuperos=float(recL),pace=paceL)
tasaRecV = StatsAdvance.tREC(self,recuperos=float(recV),pace=paceV)

#Perdidas
tasaPerdidasL = StatsAdvance.tPER(self,perdidas=float(perL),pace=paceL)
tasaPerdidasV = StatsAdvance.tPER(self,perdidas=float(perV),pace=paceV)

#Ocasiones TL
opTLL = StatsAdvance.opTL(self,tiroslibresconvertidos=float(tlcL),tiroscampointentados=float(tciL))
opTLV = StatsAdvance.opTL(self,tiroslibresconvertidos=float(tlcV),tiroscampointentados=float(tciV))

if (int(puntosL) > int(puntosV)):
    ganaA = 1
    ganaB = 0
else:
    ganaB = 1
    ganaA = 0

totales = Estadistica_Equipo_Partido.objects.create(id_partido = partido, 
                                                    id_equipo = equipoA,
                                                    puntos = puntosL,
                                                    tiros_campo_convertidos = tccL,
                                                    tiros_campo_intentados = tciL,
                                                    tiros_campo_porcentaje = tcpL,
                                                    tiros_2_convertidos = p2cL,
                                                    tiros_2_intentados = p2iL,
                                                    tiros_2_porcentaje = p2pL,
                                                    tiros_3_convertidos = p3cL,
                                                    tiros_3_intentados = p3iL,
                                                    tiros_3_porcentaje = p3pL,
                                                    tiro_libre_convertido = tlcL,
                                                    tiro_libre_intentado = tliL,
                                                    tiros_libre_porcentaje = tlpL,
                                                    rebote_ofensivo = roL,
                                                    rebote_defensivo = rdL,
                                                    rebote_total = rtL,
                                                    asistencias = asistL,
                                                    perdidas = perL,
                                                    recuperos = recL,
                                                    tapones = tapL,
                                                    faltas_personales = fpL,
                                                    valoración = valL,
                                                    pace = paceL,
                                                    eficiencia_tiro_campo = eFGL,
                                                    true_shooting = tiroRealL,
                                                    eficiencia_ofensiva = efOfensivaL,
                                                    eficiencia_defensiva = efDefensivaL,
                                                    tasa_rebote_ofensivo = tasaROL,
                                                    tasa_rebote_defensivo = tasaRDL,
                                                    tasa_recuperos = tasaRecL,
                                                    tasa_asistencias = tasaAsisL,
                                                    tasa_perdidas = tasaPerdidasL,
                                                    oportunidad_tiro_libre = opTLL,
                                                    puntos_de_perdidas = ptsPerdidasA,
                                                    puntos_pintura = ptsPinturaA,
                                                    puntos_contraataque = ptsContraataqueA,
                                                    puntos_banca = ptsBancaA,
                                                    partido_ganado = ganaA)

totales = Estadistica_Equipo_Partido.objects.create(id_partido = partido, 
                                                    id_equipo = equipoB,
                                                    puntos = puntosV,
                                                    tiros_campo_convertidos = tccV,
                                                    tiros_campo_intentados= tciV,
                                                    tiros_campo_porcentaje = tcpV,
                                                    tiros_2_convertidos = p2cV,
                                                    tiros_2_intentados = p2iV,
                                                    tiros_2_porcentaje = p2pV,
                                                    tiros_3_convertidos = p3cV,
                                                    tiros_3_intentados = p3iV,
                                                    tiros_3_porcentaje = p3pV,
                                                    tiro_libre_convertido = tlcV,
                                                    tiro_libre_intentado = tliV,
                                                    tiros_libre_porcentaje = tlpV,
                                                    rebote_ofensivo = roV,
                                                    rebote_defensivo = rdV,
                                                    rebote_total = rtV,
                                                    asistencias = asistV,
                                                    perdidas = perV,
                                                    recuperos = recV,
                                                    tapones = tapV,
                                                    faltas_personales = fpV,
                                                    valoración = valV,
                                                    pace = (paceV,2),
                                                    eficiencia_tiro_campo = eFGV,
                                                    true_shooting = tiroRealV,
                                                    eficiencia_ofensiva = efOfensivaV,
                                                    eficiencia_defensiva = efDefensivaV,
                                                    tasa_rebote_ofensivo = tasaROV,
                                                    tasa_rebote_defensivo = tasaRDV,
                                                    tasa_recuperos = tasaRecV,
                                                    tasa_asistencias = tasaAsisV,
                                                    tasa_perdidas = tasaPerdidasV,
                                                    oportunidad_tiro_libre = opTLV,
                                                    puntos_de_perdidas = ptsPerdidasB,
                                                    puntos_pintura = ptsPinturaB,
                                                    puntos_contraataque = ptsContraataqueB,
                                                    puntos_banca = ptsBancaB,
                                                    partido_ganado = ganaB)
browser.close()