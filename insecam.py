#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm
import os, sys
import ftplib
from time import *

#Variablen:
land = ["DE", "US", "FR", "JP", "IT", "TR", "GB", "NL", "KR", "RU", "CZ", "TW", "CA", "IL", "AT", "IN", "CH", "ES", "SE", "PL", "NO", "RO", "BR", "AU", "ID", "VN", "UA", "MX", "EG", "AR", "IR", "TH", "DK", "SK", "BG", "FI", "IE", "HU", "HK", "CN", "CO", "CL", "GR", "ZA", "BE", "PT", "RS", "IS", "PK", "NZ", "LV", "SG", "EE", "AE", "FO", "PS", "LT", "MY", "SI", "KW", "SV", "TN", "PA", "GE", "PH", "TT", "CR", "MD", "KE", "KH", "DO", "HR", "EC", "LU", "MT", "VE", "CY", "NI", "BD", "KZ", "NP", "RE", "MN", "MA", "GT", "SA", "BY", "JO", "PY", "PE", "AM", "CW", "HN", "AL", "BO", "BS", "NC", "AG", "UY", "LI", "SR", "BA", "JE", "GY", "PR", "GU", "QA", "LB", "GP", "BQ", "BH", "BN", "AZ", "AW", "BJ", "MO", "TG", "GL", "AD", "ME", "MC", "MQ", "JM", "HT", "PF"]
speicherort = '/var/www/html/'
dateiname = 'Marker.js'

t1 = clock()

with open (dateiname, 'w') as out:  
  def upload(ftp, file):
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
      ftp.storlines("STOR " + file, open(file))
    else:
      ftp.storbinary("STOR " + file, open(file, "rb"), 1024)
  
  out.write('var locations = [')
  for y in range (0, len(land)):
    try: #Befehlszeile lÃ¶schen
      s = sys.winver
      os.system("cls")
    except:
      os.system("clear")
    print "Scanne Land Nr " + str(y + 1) + " von " + str(len(land)) + " LÃ¤ndern.\nAktuelles Land ist " + str(land[y])
    lat = []
    lon = []
    city = []
    stream = []
    url = []
    r = requests.get('http://www.insecam.org/en/bycountry/' + str(land[y]) +'/?page=1', headers={'user-agent': 'mozilla'}) #Seitenannzahl bestimmen
    try:
      seiten = r.text.split('pagenavigator("?page=", ')[1].split(",")[0]
    except:
      seiten = 0
    for i in tqdm(range(1, int(seiten) + 1)): #Webcamannzahl und Webcamurl bestimmem
      r = requests.get('http://www.insecam.org/en/bycountry/' + str(land[y]) +'/?page=' + str(i), headers={'user-agent': 'mozilla'})
      for x in range (0, r.text.count('/en/view/')):
        url.append(str(r.text.split('/en/view/')[x+1].split('/"')[0]))

    pbar = tqdm(url)
    for char in pbar: #Webcam Url aufrufen und Kordinaten und Stream url suchen
      pbar.set_description(char)
      r = requests.get('http://www.insecam.org/en/view/' + char, headers={'user-agent': 'mozilla'})
      lat.append(r.text.split("Latitude:")[1].split('">\n')[1].split("\n<")[0])
      lon.append(r.text.split("Longitude:")[1].split('">\n')[1].split("\n<")[0])
      city.append(r.text.split('City:')[1].split('View online network cameras in ')[1].split('"')[0])
      stream.append(r.text.split('<img id="image0" src="')[1].split('"')[0])
    for i in tqdm(range(0, len(url))):
      out.write('\n        ["<a href=\'' + str(stream[i]) + '\'><img id=\'image0\' src=\'' + str(stream[i]) + '\' alt=\'\' height=\'420\' width=\'420\'/><b>' + str(city[i]) + '</b></a>", ' + str(lat[i]) + ', ' + str(lon[i]) + ', "' + str(stream[i]) + '"],')
  
  out.seek(-1, 2)
  out.write("];")
  out.close()
os.system("sudo mv " + dateiname + " " + speicherort)
t2 = clock()
dt = t2 - t1
print 'Zeit zum Erzeugen: '+str(dt)+'s'
