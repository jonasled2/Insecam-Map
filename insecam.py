#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Made by Jonas Leder
# Please check the path in the variable "speicherort" and the Name in the Variable "Dateiname" maybe this is other on your system.


#Check if needed librarys are installed and import them
try:
    import requests
    from tqdm import tqdm
    import os
    import sys
    from time import *
    from termcolor import colored

except: # Error if some librarys are missing
    print "Some librarys are not installed on your System please check, that you have installed termcolor, tqdm, tequests, time, os, sys"

#Variables:
land = ["DE", "US", "FR", "JP", "IT", "TR", "GB", "NL", "KR", "RU", "CZ", "TW", "CA", "IL", "AT", "IN", "CH", "ES", "SE", "PL", "NO", "RO", "BR", "AU", "ID", "VN", "UA", "MX", "EG", "AR", "IR", "TH", "DK", "SK", "BG", "FI", "IE", "HU", "HK", "CN", "CO", "CL", "GR", "ZA", "BE", "PT", "RS", "IS", "PK", "NZ", "LV", "SG", "EE", "AE", "FO", "PS", "LT", "MY", "SI", "KW", "SV", "TN", "PA", "GE", "PH", "TT", "CR", "MD", "KE", "KH", "DO", "HR", "EC", "LU", "MT", "VE", "CY", "NI", "BD", "KZ", "NP", "RE", "MN", "MA", "GT", "SA", "BY", "JO", "PY", "PE", "AM", "CW", "HN", "AL", "BO", "BS", "NC", "AG", "UY", "LI", "SR", "BA", "JE", "GY", "PR", "GU", "QA", "LB", "GP", "BQ", "BH", "BN", "AZ", "AW", "BJ", "MO", "TG", "GL", "AD", "ME", "MC", "MQ", "JM", "HT", "PF"]
speicherort = '/var/www/insecam/'
dateiname = 'Marker.js'
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' #Useragent from Google Chrome 65.0.3325 on windows
anzahl = 0


def clear():
    try: #clear output
      sys.winver # on linux systems
      os.system("cls")
    except:
      os.system("clear") # on windows systems
    print "Scanning country nuber " + str(y + 1) + " from " + str(len(land)) + " countrys.\nActual country is  " + str(land[y])

with open (dateiname, 'w') as out:

  out.write('var locations = [')
  for y in range (0, len(land)):
    clear()
    lat = [] #clear temp variables
    lon = []
    city = []
    stream = []
    url = []

    r = requests.get('http://www.insecam.org/en/bycountry/' + str(land[y]) +'/?page=1', headers={'user-agent': useragent}) #get number of pages
    try:
      seiten = r.text.split('pagenavigator("?page=", ')[1].split(",")[0]

    except:
      seiten = 0 # Sometimes there are no detected Cameras in a country

    print colored("[", "white"), colored('doing', 'yellow'), colored("] Scanne Seiten", "white")
    print colored("[", "white"), colored('waiting', 'cyan'), colored("] Scanne Kameras", "white")

    for i in tqdm(range(1, int(seiten) + 1)): #collect the URLs to the webcam pages
      r = requests.get('http://www.insecam.org/en/bycountry/' + str(land[y]) +'/?page=' + str(i), headers={'user-agent': useragent}) # call the search page
      for x in range (0, r.text.count('/en/view/')): # find the URL for all Cameras on that pages (usual 6)
        url.append(str(r.text.split('/en/view/')[x+1].split('/"')[0]))

    pbar = tqdm(url)

    clear()
    print colored("[", "white"), colored('OK', 'green'), colored("] Scanne Seiten", "white")
    print colored("[", "white"), colored('doing', 'yellow'), colored("] Scanne Kameras", "white")

    for char in pbar: #Call the URL and read out the Stream URL, the City and the possition
      r = requests.get('http://www.insecam.org/en/view/' + char, headers={'user-agent': useragent})
      lat.append(r.text.split("Latitude:")[1].split('">\n')[1].split("\n<")[0]) # Find the position (based on IP)
      lon.append(r.text.split("Longitude:")[1].split('">\n')[1].split("\n<")[0])
      city.append(r.text.split('City:')[1].split('View online network cameras in ')[1].split('"')[0] + "</a> <a href='http://www.insecam.org/en/view/" + char + "'>ID:" + char) # find the City
      stream.append(r.text.split('<img id="image0" src="')[1].split('"')[0]) # Find the Stream URL
      anzahl = anzahl + 1 # Count up the Cameras ( for the Comment at the End of the generatest js file)

    clear()
    print colored("[", "white"), colored('OK', 'green'), colored("] Scanne Seiten", "white")
    print colored("[", "white"), colored('OK', 'green'), colored("] Scanne Kameras", "white")

    for i in tqdm(range(0, len(url))): #Write the variables to the file and add the proxy for the Streams
      out.write('\n        ["<a href=\'' + str(stream[i]) + '\'><img id=\'image0\' src=\'https://insecam.jonasled.tk/proxy/?q=' + str(stream[i]) + '\' alt=\'\' height=\'420\' width=\'420\'/><b>' + str(city[i]) + '</b></a>", ' + str(lat[i]) + ', ' + str(lon[i]) + ', "' + str(stream[i]) + '"],')
  out.seek(-1, 2)
  out.write("\n]; /* Time: " + strftime("%d.%m.%Y %H:%M:%S") + " found cameras: " + str(anzahl) + " */") # Add a comment at the end of the file for statistic
  out.close()
os.system("sudo mv " + dateiname + " " + speicherort) # Move the the file to the output folder.
