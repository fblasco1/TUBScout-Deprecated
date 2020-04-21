import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StatsAdvance.settings.local")
import django
from selenium import webdriver 
import pandas as pd
import chromedriver_binary
from bs4 import BeautifulSoup


django.setup()

from apps.tfb.models import Equipos, Jugadores

options = webdriver.ChromeOptions()
options.add_argument('headless')

browser = webdriver.Chrome(options=options)
url = input('Ingrese el link del partido: ')
browser.get(url)

soup = BeautifulSoup(browser.page_source, "lxml")

#INSERT EQUIPO
elocal = soup.find('span',attrs = {'class':'id_aj_1_name'}).getText()
evisitante = soup.find('span',attrs = {'class': 'id_aj_2_name'}).getText()

for logo in soup.find_all('span',attrs = {'class':'id_aj_1_logoT'}):
        for url in logo.find_all('img'):
            urlLogo = url['src']

equipoA, createdA = Equipos.objects.get_or_create(nombre__exact = elocal, defaults={'nombre':elocal,'zona':'Metropolitana','urlLogo':urlLogo})

for logo in soup.find_all('span',attrs = {'class':'id_aj_2_logoT'}):
        for url in logo.find_all('img'):
            urlLogo = url['src']

equipoB, createdB = Equipos.objects.get_or_create(nombre__exact = evisitante, defaults={'nombre': evisitante, 'zona':'Metropolitana','urlLogo':urlLogo})

#Equipo A

#INSERT JUGADOR

for local in soup.find_all('a', attrs = {'tno':'1'}):
    if local.get('pno') is '0':
        print(elocal)
    else:
        nombre = soup.find('span', id = 'aj_1_'+local.get('pno')+'_name').getText()
        for imagen in soup.find_all('span', id = 'aj_1_'+local.get('pno')+'_photoT'):
            urlIMG = ''
            for url in imagen.find_all('img'):
                urlIMG = url['src']
        jugador, c = Jugadores.objects.get_or_create(id_equipo = equipoA, id_jugador = local.get('pno'), defaults = {'id_equipo':equipoA, 'id_jugador':local.get('pno'),'nombre': nombre ,'urlIMG':urlIMG})

for visitante in soup.find_all('a', attrs = {'tno':'2'}):
    if local.get('pno') is '0':
        print(evisitante)
    else:
        nombre = soup.find('span', id = 'aj_2_'+visitante.get('pno')+'_name').getText()
        for imagen in soup.find_all('span', id = 'aj_2_'+visitante.get('pno')+'_photoT'):
            urlIMG = ''
            for url in imagen.find_all('img'):
                urlIMG = url['src']
        jugador, c = Jugadores.objects.get_or_create(id_equipo = equipoB, id_jugador = visitante.get('pno'), defaults = {'id_equipo':equipoB,'id_jugador':visitante.get('pno'),'nombre': nombre ,'urlIMG':urlIMG})
    
browser.close()
