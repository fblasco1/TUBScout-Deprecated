import scrapy
import json
from scrapy.http.request import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from apps.tfb.models import Partidos
from scraper.items import PartidoItem, EquipoItem, JugadorItem,StatsTeamItem, StatsPlayerItem 

class PartidosSpider(CrawlSpider):
    name = 'partidos'
    allowed_domains = ['www.argentina.basketball', 'www.fibalivestats.com']
    start_urls = (
        """
             Links fixture
        """
        'https://www.argentina.basketball/tfb/fixture/de/division-centro',
        'https://www.argentina.basketball/tfb/fixture/de/entre-rios',
        'https://www.argentina.basketball/tfb/fixture/de/nea',
        'https://www.argentina.basketball/tfb/fixture/de/noa',
        'https://www.argentina.basketball/tfb/fixture/de/division-buenos-aires',
        'https://www.argentina.basketball/tfb/fixture/de/cuyo',
        'https://www.argentina.basketball/tfb/fixture/de/metropolitana',
        'https://www.argentina.basketball/tfb/fixture/de/patagonia',
    )
    
    rules  = (
        Rule(LinkExtractor(restrict_xpaths=('//*[contains(@href,"https://www.argentina.basketball/tfb/partido/")]')), 
        callback= 'parse_detalle'), #RULE 1 GAME PAGE
    )
    
    def parse_detalle(self,response):       
        """
            Here extract Game Info & Request DATA.JSON
        """
        partido = ItemLoader(item=PartidoItem(), response= response)

        matchId = response.xpath('//*[contains(@src,"www.fibalivestats.com/")]/@src').extract().pop().split('/')[5]

        partido.add_value('id_partido', matchId)
        partido.add_xpath('detalle_partido', '//*[@id="page_wrapper"]/section/div/div/div/div[1]/h4/text()[1]')
           
        yield partido.load_item()

class TeamsSpider(scrapy.Spider):
    name = 'teams'
    
    def start_requests(self):
        for partido in Partidos.objects.all():
            url = ('http://www.fibalivestats.com/data/'+ str(partido.id_partido) + '/data.json') 
            yield Request(url=url,callback= self.parse_fiba)

    def parse_fiba(self,response):
        equipo = ItemLoader(item=EquipoItem(), response=response)
        
        jsonresponse = json.loads(response.text)

        equipo.add_value('nombre_largo', jsonresponse['tm']['1']['name'])
        equipo.add_value('nombre_corto', jsonresponse['tm']['1']['shortName'])
        equipo.add_value('urlLogo', jsonresponse['tm']['1']['logoT']['url'])
        yield equipo.load_item()

class JugadoresSpider(scrapy.Spider):
    name = 'jugadores'
    
    def start_requests(self):
        for partido in Partidos.objects.all():
            url = ('http://www.fibalivestats.com/data/'+ str(partido.id_partido) + '/data.json') 
            yield Request(url=url,callback= self.parse_fiba)

    def parse_fiba(self,response):
        plantel  = ItemLoader(item=JugadorItem(), response= response)

        jsonresponse = json.loads(response.text)
        
        equipoA = jsonresponse['tm']['1']['name']
        equipoB = jsonresponse['tm']['2']['name']

        #PLANTEL
        #JUGADORES A
        pno = jsonresponse['tm']['1']['pl'].keys()
        
        for player in pno:
            try: 
                foto= jsonresponse['tm']['1']['pl'][player]['photoT'].replace('\/','/')
            except KeyError:
                foto= 1
            
            plantel.add_value('id_jugador', player)
            plantel.add_value('nombre', jsonresponse['tm']['1']['pl'][player]['firstName'])
            plantel.add_value('apellido', jsonresponse['tm']['1']['pl'][player]['familyName'])
            plantel.add_value('equipo', equipoA)
            plantel.add_value('urlIMG',  foto)
        
        pno = jsonresponse['tm']['2']['pl'].keys()
    
        for player in pno:
            try: 
                foto = jsonresponse['tm']['2']['pl'][player]['photoT'].replace('\/','/')
            except KeyError:
                foto = 1

            plantel.add_value('id_jugador', player)
            plantel.add_value('nombre', jsonresponse['tm']['2']['pl'][player]['firstName'])
            plantel.add_value('apellido', jsonresponse['tm']['2']['pl'][player]['familyName'])
            plantel.add_value('equipo', equipoB)
            plantel.add_value('urlIMG', foto)
        
        yield plantel.load_item()
        
class StatsSpider(scrapy.Spider):
    name = 'stats'
    
    def start_requests(self):
        for partido in Partidos.objects.all():
            url = ('http://www.fibalivestats.com/data/'+ str(partido.id_partido) + '/data.json') 
            yield Request(url=url,callback= self.parse_fiba)

    def parse_fiba(self,response):
        """
            Stats del partido
        """
      #  equipo   = ItemLoader(item=StatsTeamItem(), response= response)
        jugador  = ItemLoader(item=StatsPlayerItem(), response= response)
        
        jsonresponse = json.loads(response.text)

        matchId = response.url.split('/')[4]

        nombrelargoA = jsonresponse['tm']['1']['name']
        nombrelargoB = jsonresponse['tm']['2']['name']
        nombrecortoA = jsonresponse['tm']['1']['shortName']
        nombrecortoB = jsonresponse['tm']['2']['shortName']
        """
        #STATS EQUIPOS
        equipo.add_value('id_partido', matchId)
        equipo.add_value('equipoA', equipoA)
        equipo.add_value('local', 1)
        equipo.add_value('puntosA', jsonresponse['tm']['1']['score'])
        equipo.add_value('q1A', jsonresponse['tm']['1']['p1_score'])
        equipo.add_value('q2A', jsonresponse['tm']['1']['p2_score'])
        equipo.add_value('q3A', jsonresponse['tm']['1']['p3_score'])
        equipo.add_value('q4A', jsonresponse['tm']['1']['p4_score'])
        equipo.add_value('tccA', jsonresponse['tm']['1']['tot_sFieldGoalsMade'])
        equipo.add_value('tciA', jsonresponse['tm']['1']['tot_sFieldGoalsAttempted'])
        equipo.add_value('tcpA', jsonresponse['tm']['1']['tot_sFieldGoalsPercentage'])
        equipo.add_value('t2cA', jsonresponse['tm']['1']['tot_sTwoPointersMade'])
        equipo.add_value('t2iA', jsonresponse['tm']['1']['tot_sTwoPointersAttempted'])
        equipo.add_value('t2pA', jsonresponse['tm']['1']['tot_sTwoPointersPercentage'])
        equipo.add_value('t3cA', jsonresponse['tm']['1']['tot_sThreePointersMade'])
        equipo.add_value('t3iA', jsonresponse['tm']['1']['tot_sThreePointersAttempted'])
        equipo.add_value('t3pA', jsonresponse['tm']['1']['tot_sThreePointersPercentage'])
        equipo.add_value('tlcA', jsonresponse['tm']['1']['tot_sFreeThrowsMade'])
        equipo.add_value('tliA', jsonresponse['tm']['1']['tot_sFreeThrowsAttempted'])
        equipo.add_value('tlpA', jsonresponse['tm']['1']['tot_sFreeThrowsPercentage'])
        equipo.add_value('roA', jsonresponse['tm']['1']['tot_sReboundsOffensive'])
        equipo.add_value('rdA', jsonresponse['tm']['1']['tot_sReboundsDefensive'])
        equipo.add_value('rtA', jsonresponse['tm']['1']['tot_sReboundsTotal'])
        equipo.add_value('asisA', jsonresponse['tm']['1']['tot_sAssists'])
        equipo.add_value('perA', jsonresponse['tm']['1']['tot_sTurnovers'])
        equipo.add_value('recA', jsonresponse['tm']['1']['tot_sSteals'])
        equipo.add_value('tapA', jsonresponse['tm']['1']['tot_sBlocks'])
        equipo.add_value('fpA', jsonresponse['tm']['1']['tot_sFoulsTotal'])
        equipo.add_value('valA', jsonresponse['tm']['1']['tot_eff_1'])
        equipo.add_value('puntos_bancaA', jsonresponse['tm']['1']['tot_sBenchPoints'])
        equipo.add_value('puntos_contraataqueA', jsonresponse['tm']['1']['tot_sPointsFastBreak'])
        equipo.add_value('puntos_de_perdidasA', jsonresponse['tm']['1']['tot_sPointsFromTurnovers'])
        equipo.add_value('puntos_pinturaA', jsonresponse['tm']['1']['tot_sPointsInThePaint'])
        equipo.add_value('puntos_roA', jsonresponse['tm']['1']['tot_sPointsSecondChance'])
        #EQUIPO B
        equipo.add_value('equipoB', equipoB)
        equipo.add_value('visitante', 0)
        equipo.add_value('puntosB', jsonresponse['tm']['2']['score'])
        equipo.add_value('q1B', jsonresponse['tm']['2']['p1_score'])
        equipo.add_value('q2B', jsonresponse['tm']['2']['p2_score'])
        equipo.add_value('q3B', jsonresponse['tm']['2']['p3_score'])
        equipo.add_value('q4B', jsonresponse['tm']['2']['p4_score'])
        equipo.add_value('tccB', jsonresponse['tm']['2']['tot_sFieldGoalsMade'])
        equipo.add_value('tciB', jsonresponse['tm']['2']['tot_sFieldGoalsAttempted'])
        equipo.add_value('tcpB', jsonresponse['tm']['2']['tot_sFieldGoalsPercentage'])
        equipo.add_value('t2cB', jsonresponse['tm']['2']['tot_sTwoPointersMade'])
        equipo.add_value('t2iB', jsonresponse['tm']['2']['tot_sTwoPointersAttempted'])
        equipo.add_value('t2pB', jsonresponse['tm']['2']['tot_sTwoPointersPercentage'])
        equipo.add_value('t3cB', jsonresponse['tm']['2']['tot_sThreePointersMade'])
        equipo.add_value('t3iB', jsonresponse['tm']['2']['tot_sThreePointersAttempted'])
        equipo.add_value('t3pB', jsonresponse['tm']['2']['tot_sThreePointersPercentage'])
        equipo.add_value('tlcB', jsonresponse['tm']['2']['tot_sFreeThrowsMade'])
        equipo.add_value('tliB', jsonresponse['tm']['2']['tot_sFreeThrowsAttempted'])
        equipo.add_value('tlpB', jsonresponse['tm']['2']['tot_sFreeThrowsPercentage'])
        equipo.add_value('roB', jsonresponse['tm']['2']['tot_sReboundsOffensive'])
        equipo.add_value('rdB', jsonresponse['tm']['2']['tot_sReboundsDefensive'])
        equipo.add_value('rtB', jsonresponse['tm']['2']['tot_sReboundsTotal'])
        equipo.add_value('asisB', jsonresponse['tm']['2']['tot_sAssists'])
        equipo.add_value('perB', jsonresponse['tm']['2']['tot_sTurnovers'])
        equipo.add_value('recB', jsonresponse['tm']['2']['tot_sSteals'])
        equipo.add_value('tapB', jsonresponse['tm']['2']['tot_sBlocks'])
        equipo.add_value('fpB', jsonresponse['tm']['2']['tot_sFoulsTotal'])
        equipo.add_value('valB', jsonresponse['tm']['2']['tot_eff_1'])
        equipo.add_value('puntos_bancaB', jsonresponse['tm']['2']['tot_sBenchPoints'])
        equipo.add_value('puntos_contraataqueB', jsonresponse['tm']['2']['tot_sPointsFastBreak'])
        equipo.add_value('puntos_de_perdidasB', jsonresponse['tm']['2']['tot_sPointsFromTurnovers'])
        equipo.add_value('puntos_pinturaB', jsonresponse['tm']['2']['tot_sPointsInThePaint'])
        equipo.add_value('puntos_roB', jsonresponse['tm']['2']['tot_sPointsSecondChance'])
        yield equipo.load_item()
        """     
        #JUGADORES
        #EQUIPO A
        #STATS
        pno = jsonresponse['tm']['1']['pl'].keys()
        
        for player in pno:
            jugador.add_value('id_partido', matchId)
            jugador.add_value('id_jugador', player)
            jugador.add_value('inicial',jsonresponse['tm']['1']['pl'][player]['starter'])
            jugador.add_value('nombre', jsonresponse['tm']['1']['pl'][player]['firstName'])
            jugador.add_value('apellido', jsonresponse['tm']['1']['pl'][player]['familyName'])
            jugador.add_value('nombrelargo', nombrelargoA)
            jugador.add_value('nombrecorto', nombrecortoA)
            jugador.add_value('minutos', jsonresponse['tm']['1']['pl'][player]['sMinutes'])
            jugador.add_value('puntos', jsonresponse['tm']['1']['pl'][player]['sPoints'])
            jugador.add_value('tiros_campo_convertidos', jsonresponse['tm']['1']['pl'][player]['sFieldGoalsMade'])
            jugador.add_value('tiros_campo_intentados', jsonresponse['tm']['1']['pl'][player]['sFieldGoalsAttempted'])
            jugador.add_value('tiros_campo_porcentaje', jsonresponse['tm']['1']['pl'][player]['sFieldGoalsPercentage'])
            jugador.add_value('tiros_2_convertidos', jsonresponse['tm']['1']['pl'][player]['sTwoPointersMade'])
            jugador.add_value('tiros_2_intentados', jsonresponse['tm']['1']['pl'][player]['sTwoPointersAttempted'])
            jugador.add_value('tiros_2_porcentaje', jsonresponse['tm']['1']['pl'][player]['sTwoPointersPercentage'])
            jugador.add_value('tiros_3_convertidos', jsonresponse['tm']['1']['pl'][player]['sThreePointersMade'])
            jugador.add_value('tiros_3_intentados', jsonresponse['tm']['1']['pl'][player]['sThreePointersAttempted'])
            jugador.add_value('tiros_3_porcentaje', jsonresponse['tm']['1']['pl'][player]['sThreePointersPercentage'])
            jugador.add_value('tiro_libre_convertido', jsonresponse['tm']['1']['pl'][player]['sFreeThrowsMade'])
            jugador.add_value('tiro_libre_intentado', jsonresponse['tm']['1']['pl'][player]['sFreeThrowsAttempted'])
            jugador.add_value('tiros_libre_porcentaje', jsonresponse['tm']['1']['pl'][player]['sFreeThrowsPercentage'])
            jugador.add_value('rebote_ofensivo', jsonresponse['tm']['1']['pl'][player]['sReboundsOffensive'])
            jugador.add_value('rebote_defensivo', jsonresponse['tm']['1']['pl'][player]['sReboundsDefensive'])
            jugador.add_value('rebote_total', jsonresponse['tm']['1']['pl'][player]['sReboundsTotal'])
            jugador.add_value('asistencias', jsonresponse['tm']['1']['pl'][player]['sAssists'])
            jugador.add_value('perdidas', jsonresponse['tm']['1']['pl'][player]['sTurnovers'])
            jugador.add_value('recuperos', jsonresponse['tm']['1']['pl'][player]['sSteals'])
            jugador.add_value('tapones', jsonresponse['tm']['1']['pl'][player]['sBlocks'])
            jugador.add_value('faltas_personales', jsonresponse['tm']['1']['pl'][player]['sFoulsPersonal'])
            jugador.add_value('faltas_recibidas', jsonresponse['tm']['1']['pl'][player]['sFoulsOn'])
            jugador.add_value('diferencia_puntos',jsonresponse['tm']['1']['pl'][player]['sPlusMinusPoints'])
            jugador.add_value('valoración', jsonresponse['tm']['1']['pl'][player]['eff_1'])
        #EQUIPO B
        #STATS
        pno = jsonresponse['tm']['2']['pl'].keys()

        for player in pno:
            jugador.add_value('id_partido', matchId)
            jugador.add_value('id_jugador', player)
            jugador.add_value('inicial',jsonresponse['tm']['2']['pl'][player]['starter'])
            jugador.add_value('nombre', jsonresponse['tm']['2']['pl'][player]['firstName'])
            jugador.add_value('apellido', jsonresponse['tm']['2']['pl'][player]['familyName'])
            jugador.add_value('nombrelargo', nombrelargoB)
            jugador.add_value('nombrecorto', nombrecortoB)
            jugador.add_value('minutos', jsonresponse['tm']['2']['pl'][player]['sMinutes'])
            jugador.add_value('puntos', jsonresponse['tm']['2']['pl'][player]['sPoints'])
            jugador.add_value('tiros_campo_convertidos', jsonresponse['tm']['2']['pl'][player]['sFieldGoalsMade'])
            jugador.add_value('tiros_campo_intentados', jsonresponse['tm']['2']['pl'][player]['sFieldGoalsAttempted'])
            jugador.add_value('tiros_campo_porcentaje', jsonresponse['tm']['2']['pl'][player]['sFieldGoalsPercentage'])
            jugador.add_value('tiros_2_convertidos', jsonresponse['tm']['2']['pl'][player]['sTwoPointersMade'])
            jugador.add_value('tiros_2_intentados', jsonresponse['tm']['2']['pl'][player]['sTwoPointersAttempted'])
            jugador.add_value('tiros_2_porcentaje', jsonresponse['tm']['2']['pl'][player]['sTwoPointersPercentage'])
            jugador.add_value('tiros_3_convertidos', jsonresponse['tm']['2']['pl'][player]['sThreePointersMade'])
            jugador.add_value('tiros_3_intentados', jsonresponse['tm']['2']['pl'][player]['sThreePointersAttempted'])
            jugador.add_value('tiros_3_porcentaje', jsonresponse['tm']['2']['pl'][player]['sThreePointersPercentage'])
            jugador.add_value('tiro_libre_convertido', jsonresponse['tm']['2']['pl'][player]['sFreeThrowsMade'])
            jugador.add_value('tiro_libre_intentado', jsonresponse['tm']['2']['pl'][player]['sFreeThrowsAttempted'])
            jugador.add_value('tiros_libre_porcentaje', jsonresponse['tm']['2']['pl'][player]['sFreeThrowsPercentage'])
            jugador.add_value('rebote_ofensivo', jsonresponse['tm']['2']['pl'][player]['sReboundsOffensive'])
            jugador.add_value('rebote_defensivo', jsonresponse['tm']['2']['pl'][player]['sReboundsDefensive'])
            jugador.add_value('rebote_total', jsonresponse['tm']['2']['pl'][player]['sReboundsTotal'])
            jugador.add_value('asistencias', jsonresponse['tm']['2']['pl'][player]['sAssists'])
            jugador.add_value('perdidas', jsonresponse['tm']['2']['pl'][player]['sTurnovers'])
            jugador.add_value('recuperos', jsonresponse['tm']['2']['pl'][player]['sSteals'])
            jugador.add_value('tapones', jsonresponse['tm']['2']['pl'][player]['sBlocks'])
            jugador.add_value('faltas_personales', jsonresponse['tm']['2']['pl'][player]['sFoulsPersonal'])
            jugador.add_value('faltas_recibidas', jsonresponse['tm']['2']['pl'][player]['sFoulsOn'])
            jugador.add_value('diferencia_puntos',jsonresponse['tm']['2']['pl'][player]['sPlusMinusPoints'])
            jugador.add_value('valoración', jsonresponse['tm']['2']['pl'][player]['eff_1'])
        yield jugador.load_item()



        