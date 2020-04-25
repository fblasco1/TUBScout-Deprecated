import scrapy
from scrapy.http.request import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scraper.items import PartidoItem, StatsTeamItem, StatsPlayerItem, JugadorItem

class FibaSpider(CrawlSpider):
    name = 'fibalinks'
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

        Rule(LinkExtractor(restrict_xpaths='//*[contains(@src,"www.fibalivestats.com/")]'), 
        callback='parse_fiba'), #RULE 2 IFRAME BOXSCORE

        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div[1]/div[1]/a'),
        callback='parse_fibabs'), #RULE 3 COMPLETE BOXSCORE
    )

    def parse_detalle(self,response): 
        """
            Here extract Game Info (detalle_partido = Game Day, fibalink = BoxScore Game link) and aplicate rule 2
        """
        partido = ItemLoader(item=PartidoItem(), response= response)
        
        partido.add_xpath('detalle_partido', '//*[@id="page_wrapper"]/section/div/div/div/div[1]/h4/text()[1]')
        partido.add_xpath('fibalink', '//*[contains(@src,"www.fibalivestats.com/")]')
        
        yield partido

    def parse_fiba(self,response):
        """
            Here extract team players and aplicate rule 3
        """

        jugador  = ItemLoader(item=JugadorItem(), response= response)
    
        equipoA = response.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div/span[2]//text()').get()
        equipoB = response.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div/span[2]//text()').get()
    
        #CREATE OR UPDATE PLANTEL
        #JUGADORES A
        jugadorpno = response.xpath('//a[contains(@tno,1)]//@pno').getall()
    
        for player in jugadorpno:
            if player == 0:
                continue
            else: 
                jugador.add_xpath('id_jugador', player)
                jugador.add_xpath('nombre', '//*[@id="aj_1_'+ str(player) +'_name"]')
                jugador.add_value('equipo', equipoA)
                jugador.add_xpath('urlIMG', '//*[@id="aj_1_'+ str(player) +'_photoT"]/img//@src')
                yield jugador

        #JUGADORES B
        jugadorpno = response.xpath('//a[contains(@tno,2)]//@pno').getall()
    
        for player in jugadorpno:
            if player == 0:
                continue
            else:
                jugador.add_xpath('id_jugador', player)
                jugador.add_xpath('nombre', '//*[@id="aj_2_'+ str(player) +'_name"]')
                jugador.add_value('equipo', equipoB)
                jugador.add_xpath('urlIMG', '//*[@id="aj_2_'+ str(player) +'_photoT"]/img//@src')
                yield jugador

    def parse_fibabs(self,response):
        partido   = ItemLoader(item=StatsTeamItem(), response= response)
        jugador  = ItemLoader(item=StatsPlayerItem(), response= response)


        id_partido = response.xpath('//*[@id="matchId"]//@value')
    
        #EQUIPOS
        partido.add_value('id_partido', id_partido)
        partido.add_xpath('equipoA', '//*[@id="aj_1_name"]/text()')
        partido.add_value('local', 1)
        partido.add_xpath('puntosA','//*[@id="aj_1_tot_sPoints"]/text()')
        partido.add_xpath('tccA', '//*[@id="aj_1_tot_sFieldGoalsMade"]/text()')
        partido.add_xpath('tciA', '//*[@id="aj_1_tot_sFieldGoalsAttempted"]/text()')
        partido.add_xpath('tcpA', '//*[@id="aj_1_tot_sFieldGoalsPercentage"]/text()')
        partido.add_xpath('t2cA', '//*[@id="aj_1_tot_sTwoPointersMade"]/text()')
        partido.add_xpath('t2iA', '//*[@id="aj_1_tot_sTwoPointersAttempted"]/text()')
        partido.add_xpath('t2pA', '//*[@id="aj_1_tot_sTwoPointersPercentage"]/text()')
        partido.add_xpath('t3cA', '//*[@id="aj_1_tot_sThreePointersMade"]/text()')
        partido.add_xpath('t3iA', '//*[@id="aj_1_tot_sThreePointersAttempted"]/text()')
        partido.add_xpath('t3pA', '//*[@id="aj_1_tot_sThreePointersPercentage"]/text()')
        partido.add_xpath('tlcA', '//*[@id="aj_1_tot_sFreeThrowsMade"]/text()')
        partido.add_xpath('tliA', '//*[@id="aj_1_tot_sFreeThrowsAttempted"]/text()')
        partido.add_xpath('tlpA', '//*[@id="aj_1_tot_sFreeThrowsPercentage"]/text()')
        partido.add_xpath('roA', '//*[@id="aj_1_tot_sReboundsOffensive"]/text()')
        partido.add_xpath('rdA', '//*[@id="aj_1_tot_sReboundsDefensive"]/text()')
        partido.add_xpath('rtA', '//*[@id="aj_1_tot_sReboundsTotal"]/text()')
        partido.add_xpath('asisA', '//*[@id="aj_1_tot_sAssists"]/text()')
        partido.add_xpath('perA', '//*[@id="aj_1_tot_sTurnovers"]/text()')
        partido.add_xpath('recA', '//*[@id="aj_1_tot_sSteals"]/text()')
        partido.add_xpath('tapA', '//*[@id="aj_1_tot_sBlocks"]/text()')
        partido.add_xpath('fpA', '//*[@id="aj_1_tot_sFoulsTotal"]/text()')
        partido.add_xpath('valA', '//*[@id="aj_1_tot_eff_1"]/text()')
        partido.add_xpath('puntos_bancaA', '//*[@id="aj_1_tot_sBenchPoints"]/text()')
        partido.add_xpath('puntos_contraataqueA', '//*[@id="aj_1_tot_sPointsFastBreak"]/text()')
        partido.add_xpath('puntos_de_perdidasA', '//*[@id="aj_1_tot_sPointsFromTurnovers"]/text()')
        partido.add_xpath('puntos_pinturaA', '//*[@id="aj_1_tot_sPointsInThePaint"]/text()')
        partido.add_xpath('puntos_roA', '//*[@id="aj_1_tot_sPointsSecondChance"]/text()')
        #EQUIPO B
        partido.add_xpath('equipoB', '//*[@id="aj_2_name"]/text()')
        partido.add_value('visitante', 0)
        partido.add_value('puntosB', '//*[@id="aj_2_tot_sPoints"]/text()')
        partido.add_xpath('tccB', '//*[@id="aj_2_tot_sFieldGoalsMade"]/text()')
        partido.add_xpath('tciB', '//*[@id="aj_2_tot_sFieldGoalsAttempted"]/text()')
        partido.add_xpath('tcpB', '//*[@id="aj_2_tot_sFieldGoalsPercentage"]/text()')
        partido.add_xpath('t2cB', '//*[@id="aj_2_tot_sTwoPointersMade"]/text()')
        partido.add_xpath('t2iB', '//*[@id="aj_2_tot_sTwoPointersAttempted"]/text()')
        partido.add_xpath('t2pB', '//*[@id="aj_2_tot_sTwoPointersPercentage"]/text()')
        partido.add_xpath('t3cB', '//*[@id="aj_2_tot_sThreePointersMade"]/text()')
        partido.add_xpath('t3iB', '//*[@id="aj_2_tot_sThreePointersAttempted"]/text()')
        partido.add_xpath('t3pB', '//*[@id="aj_2_tot_sThreePointersPercentage"]/text()')
        partido.add_xpath('tlcB', '//*[@id="aj_2_tot_sFreeThrowsMade"]/text()')
        partido.add_xpath('tliB', '//*[@id="aj_2_tot_sFreeThrowsAttempted"]/text()')
        partido.add_xpath('tlpB', '//*[@id="aj_2_tot_sFreeThrowsPercentage"]/text()')
        partido.add_xpath('roB', '//*[@id="aj_2_tot_sReboundsOffensive"]/text()')
        partido.add_xpath('rdB', '//*[@id="aj_2_tot_sReboundsDefensive"]/text()')
        partido.add_xpath('rtB', '//*[@id="aj_2_tot_sReboundsTotal"]/text()')
        partido.add_xpath('asisB', '//*[@id="aj_2_tot_sAssists"]/text()')
        partido.add_xpath('perB', '//*[@id="aj_2_tot_sTurnovers"]/text()')
        partido.add_xpath('recB', '//*[@id="aj_2_tot_sSteals"]/text()')
        partido.add_xpath('tapB', '//*[@id="aj_2_tot_sBlocks"]/text()')
        partido.add_xpath('fpB', '//*[@id="aj_2_tot_sFoulsTotal"]/text()')
        partido.add_xpath('valB', '//*[@id="aj_2_tot_eff_1"]/text()')
        partido.add_xpath('puntos_bancaB', '//*[@id="aj_2_tot_sBenchPoints"]/text()')
        partido.add_xpath('puntos_contraataqueB', '//*[@id="aj_2_tot_sPointsFastBreak"]/text()')
        partido.add_xpath('puntos_de_perdidasB', '//*[@id="aj_2_tot_sPointsFromTurnovers"]/text()')
        partido.add_xpath('puntos_pinturaB', '//*[@id="aj_2_tot_sPointsInThePaint"]/text()')
        partido.add_xpath('puntos_roB', '//*[@id="aj_2_tot_sPointsSecondChance"]/text()')
        yield partido

        #JUGADORES
        jugadorpno = response.xpath('//a[contains(@tno,1)]//@pno').getall()
        
        for player in jugadorpno:
            if player == 0:
                continue
            else: 
                jugador.add_value('id_partido', id_partido)
                jugador.add_value('id_jugador', player)
                jugador.add_value('equipo', '//*[@id="aj_1_name"]/text()')
                jugador.add_xpath('minutos', '//*[@id="aj_1_'+ str(player) + '_sMinutes"]/text()')
                jugador.add_xpath('puntos', '//*[@id="aj_1_'+ str(player) + '_sPoints"]/text()')
                jugador.add_xpath('tiros_campo_convertidos', '//*[@id="aj_1_'+ str(player) +'_sFieldGoalsMade"]/text()')
                jugador.add_xpath('tiros_campo_intentados', '//*[@id="aj_1_' + str(player) + '_sFieldGoalsAttempted"]/text()')
                jugador.add_xpath('tiros_campo_porcentaje', '//*[@id="aj_1_'+ str(player) +'_sFieldGoalsPercentage"]/text()')
                jugador.add_xpath('tiros_2_convertidos', '//*[@id="aj_1_'+ str(player) +'_sTwoPointersMade"]/text()')
                jugador.add_xpath('tiros_2_intentados', '//*[@id="aj_1_' + str(player) + '_sTwoPointersAttempted"]/text()')
                jugador.add_xpath('tiros_2_porcentaje', '//*[@id="aj_1_' + str(player) + '_sTwoPointersPercentage"]/text()')
                jugador.add_xpath('tiros_3_convertidos', '//*[@id="aj_1_' + str(player) + '_sThreePointersMade"]/text()')
                jugador.add_xpath('tiros_3_intentados', '//*[@id="aj_1_' + str(player) + '_sThreePointersAttempted"]/text()')
                jugador.add_xpath('tiros_3_porcentaje', '//*[@id="aj_1_' + str(player) + '_sThreePointersPercentage"]/text()')
                jugador.add_xpath('tiro_libre_convertido', '//*[@id="aj_1_' + str(player) + '_sFreeThrowsMade"]/text()')
                jugador.add_xpath('tiro_libre_intentado', '//*[@id="aj_1_' + str(player) + '_sFreeThrowsAttempted"]/text()')
                jugador.add_xpath('tiros_libre_porcentaje', '//*[@id="aj_1_' + str(player) + '_sFreeThrowsPercentage"]/text()')
                jugador.add_xpath('rebote_ofensivo', '//*[@id="aj_1_' + str(player) + '_sReboundsOffensive"]/text()')
                jugador.add_xpath('rebote_defensivo', '//*[@id="aj_1_' + str(player) + '_sReboundsDefensive"]/text()')
                jugador.add_xpath('rebote_total', '//*[@id="aj_1_' + str(player) + '_sReboundsTotal"]/text()')
                jugador.add_xpath('asistencias', '//*[@id="aj_1_' + str(player) + '_sAssists"]/text()')
                jugador.add_xpath('perdidas', '//*[@id="aj_1_' + str(player) + '_sTurnovers"]/text()')
                jugador.add_xpath('recuperos', '//*[@id="aj_1_' + str(player) + '_sSteals"]/text()')
                jugador.add_xpath('tapones', '//*[@id="aj_1_' + str(player) + '_sBlocks"]/text()')
                jugador.add_xpath('faltas_personales', '//*[@id="aj_1_'+ str(player) +'_sFoulsPersonal"]/text()')
                jugador.add_xpath('faltas_recibidas', '//*[@id="aj_1_'+ str(player) +'_sFoulsOn"]/text()')
                jugador.add_xpath('diferencia_puntos','//*[@id="aj_1_'+ str(player) +'_sPlusMinusPoints"]/text()')
                jugador.add_xpath('valoración', '//*[@id="aj_1_' + str(player) + '_eff_1"]/text()')
                yield jugador    

        #JUGADORES
        jugadorpno = response.xpath('//a[contains(@tno,2)]//@pno').getall()
        
        for player in jugadorpno:
            if player == 0:
                continue
            else: 
                jugador.add_value('id_partido', id_partido)
                jugador.add_value('id_jugador', player)
                jugador.add_value('equipo', '//*[@id="aj_2_name"]/text()')
                jugador.add_xpath('minutos', '//*[@id="aj_2_'+ str(player) + '_sMinutes"]/text()')
                jugador.add_xpath('puntos', '//*[@id="aj_2_'+ str(player) + '_sPoints"]/text()')
                jugador.add_xpath('tiros_campo_convertidos', '//*[@id="aj_2_'+ str(player) +'_sFieldGoalsMade"]/text()')
                jugador.add_xpath('tiros_campo_intentados', '//*[@id="aj_2_' + str(player) + '_sFieldGoalsAttempted"]/text()')
                jugador.add_xpath('tiros_campo_porcentaje', '//*[@id="aj_2_'+ str(player) +'_sFieldGoalsPercentage"]/text()')
                jugador.add_xpath('tiros_2_convertidos', '//*[@id="aj_2_'+ str(player) +'_sTwoPointersMade"]/text()')
                jugador.add_xpath('tiros_2_intentados', '//*[@id="aj_2_' + str(player) + '_sTwoPointersAttempted"]/text()')
                jugador.add_xpath('tiros_2_porcentaje', '//*[@id="aj_2_' + str(player) + '_sTwoPointersPercentage"]/text()')
                jugador.add_xpath('tiros_3_convertidos', '//*[@id="aj_2_' + str(player) + '_sThreePointersMade"]/text()')
                jugador.add_xpath('tiros_3_intentados', '//*[@id="aj_2_' + str(player) + '_sThreePointersAttempted"]/text()')
                jugador.add_xpath('tiros_3_porcentaje', '//*[@id="aj_2_' + str(player) + '_sThreePointersPercentage"]/text()')
                jugador.add_xpath('tiro_libre_convertido', '//*[@id="aj_2_' + str(player) + '_sFreeThrowsMade"]/text()')
                jugador.add_xpath('tiro_libre_intentado', '//*[@id="aj_2_' + str(player) + '_sFreeThrowsAttempted"]/text()')
                jugador.add_xpath('tiros_libre_porcentaje', '//*[@id="aj_2_' + str(player) + '_sFreeThrowsPercentage"]/text()')
                jugador.add_xpath('rebote_ofensivo', '//*[@id="aj_2_' + str(player) + '_sReboundsOffensive"]/text()')
                jugador.add_xpath('rebote_defensivo', '//*[@id="aj_2_' + str(player) + '_sReboundsDefensive"]/text()')
                jugador.add_xpath('rebote_total', '//*[@id="aj_2_' + str(player) + '_sReboundsTotal"]/text()')
                jugador.add_xpath('asistencias', '//*[@id="aj_2_' + str(player) + '_sAssists"]/text()')
                jugador.add_xpath('perdidas', '//*[@id="aj_2_' + str(player) + '_sTurnovers"]/text()')
                jugador.add_xpath('recuperos', '//*[@id="aj_2_' + str(player) + '_sSteals"]/text()')
                jugador.add_xpath('tapones', '//*[@id="aj_2_' + str(player) + '_sBlocks"]/text()')
                jugador.add_xpath('faltas_personales', '//*[@id="aj_2_'+ str(player) +'_sFoulsPersonal"]/text()')
                jugador.add_xpath('faltas_recibidas', '//*[@id="aj_2_'+ str(player) +'_sFoulsOn"]/text()')
                jugador.add_xpath('diferencia_puntos','//*[@id="aj_2_'+ str(player) +'_sPlusMinusPoints"]/text()')
                jugador.add_xpath('valoración', '//*[@id="aj_2_' + str(player) + '_eff_1"]/text()')
                yield jugador