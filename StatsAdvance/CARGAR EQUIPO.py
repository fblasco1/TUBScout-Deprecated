import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StatsAdvance.settings.local")
import django
from selenium import webdriver 
import pandas as pd
import chromedriver_binary
from bs4 import BeautifulSoup

django.setup()

from apps.tfb.models import Equipos

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

equipoA, createdA = Equipos.objects.get_or_create(nombre__exact = elocal, defaults={'nombre':elocal,'zona':'NOA','urlLogo':urlLogo})

for logo in soup.find_all('span',attrs = {'class':'id_aj_2_logoT'}):
        for url in logo.find_all('img'):
            urlLogo = url['src']

equipoB, createdB = Equipos.objects.get_or_create(nombre__exact = evisitante, defaults={'nombre': evisitante, 'zona':'NOA','urlLogo':urlLogo})

browser.close()
