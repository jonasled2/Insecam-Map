#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm
import os, sys
import ftplib

#Variablen:
land = ''
api_key = ''
ftp_server = ''
ftp_username = ''
ftp_password = ''
speicherort = ''
dateiname = ''
with open (dateiname, 'w') as out:  
  def upload(ftp, file):
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
      ftp.storlines("STOR " + file, open(file))
    else:
      ftp.storbinary("STOR " + file, open(file, "rb"), 1024)
      
  try: #Befehlszeile löschen
      s = sys.winver
      os.system("cls")
  except:
    os.system("clear")
  
  out.write('   <!DOCTYPE html>\n   <html>\n   <head>\n     <meta http-equiv="content-type" content="text/html; charset=ANSI" />\n     <title>Insecam Map</title>\n	 <style>\n      /* Always set the map height explicitly to define the size of the div\n       * element that contains the map. */\n      #map {\n        height: 100%;\n      }\n      /* Optional: Makes the sample page fill the window. */\n      html, body {\n        height: 100%;\n        margin: 0;\n        padding: 0;\n      }\n    </style>\n   </head>\n   <body>\n     <div id="map"div>\n		<script src="https://maps.googleapis.com/maps/api/js?key=' + str(api_key) + '"\n      type="text/javascript"></script>\n     <script type="text/javascript">\n       var locations = [\n')
  url = []
  r = requests.get('http://www.insecam.org/en/bycountry/' + str(land) +'/?page=1', headers={'user-agent': 'mozilla'}) #Seitenannzahl bestimmen
  seiten = r.text.split('pagenavigator("?page=", ')[1].split(",")[0]
  for i in tqdm(range(1, int(seiten) + 1)): #Webcamannzahl und Webcamurl bestimmem
    r = requests.get('http://www.insecam.org/en/bycountry/' + str(land) +'/?page=' + str(i), headers={'user-agent': 'mozilla'})
    for x in range (0, r.text.count('/en/view/')):
      url.append(str(r.text.split('/en/view/')[x+1].split('/"')[0]))

  for i in tqdm(range(0, len(url))): #Webcam Url aufrufen und Kordinaten und Stream url suchen
    r = requests.get('http://www.insecam.org/en/view/' + url[i], headers={'user-agent': 'mozilla'})
    lat = r.text.split("Latitude:")[1].split('">\n')[1].split("\n<")[0]
    lon = r.text.split("Longitude:")[1].split('">\n')[1].split("\n<")[0]
    city = r.text.split('City:')[1].split('View online network cameras in ')[1].split('"')[0]
    stream = r.text.split('<img id="image0" src="')[1].split('"')[0]
    if (i == len(url) - 1):
      out.write('        ["<a href=\'' + str(stream) + '\'><img id=\'image0\' src=\'' + str(stream) + '\' alt=\'\' height=\'420\' width=\'420\'/><b>' + str(city) + '</b></a>", ' + str(lat) + ', ' + str(lon) + ', "' + str(stream) + '"]];\n')
    if (i != len(url) - 1):
      out.write('        ["<a href=\'' + str(stream) + '\'><img id=\'image0\' src=\'' + str(stream) + '\' alt=\'\' height=\'420\' width=\'420\'/><b>' + str(city) + '</b></a>", ' + str(lat) + ', ' + str(lon) + ', "' + str(stream) + '"],\n')
  out.write('var map = new google.maps.Map(document.getElementById("map"), {\n  zoom: 5,\n center: new google.maps.LatLng(51.54376, 9.910419999999931),\n mapTypeId: google.maps.MapTypeId.ROADMAP\n});\n        if (navigator.geolocation) {\n          navigator.geolocation.getCurrentPosition(function(position) {\n            var pos = {\n              lat: position.coords.latitude,\n              lng: position.coords.longitude\n            };\n			map.setZoom(11);\n            map.setCenter(pos);\n          }, function() {\n            handleLocationError(true, infoWindow, map.getCenter());\n          });\n        } else {\n          handleLocationError(false, infoWindow, map.getCenter());\n        }\nvar infowindow = new google.maps.InfoWindow();\n\nvar marker, i;\n\nfor (i = 0; i < locations.length; i++) {\n  marker = new google.maps.Marker({\n   position: new google.maps.LatLng(locations[i][1], locations[i][2]),\n   map: map,\n   url: locations[i][3]\n  });\n\n      google.maps.event.addListener(marker, "click", (function(marker, i) {\n   return function() {\n     infowindow.setContent(locations[i][0]);\n     infowindow.open(map, marker);\n   }\n })(marker, i));\n\n    }\n\n     </script>\n	 <!-- Google Analytics -->\n	<script>\n	(function(i,s,o,g,r,a,m){i["GoogleAnalyticsObject"]=r;i[r]=i[r]||function(){\n	(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\n	m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\n	})(window,document,"script","https://www.google-analytics.com/analytics.js","ga");\n\n	ga("create", "UA-110852907-1", "auto");\n	ga("send", "pageview");\n	</script>\n	<!-- End Google Analytics -->\n   </body>\n   </html>\n')
  out.close()
ftp = ftplib.FTP(ftp_server) #fertige html Datei über ftp hochladen
ftp.login(ftp_username, ftp_password)
ftp.cwd(speicherort) 
upload(ftp, dateiname)
print "upload auf FTP Server abgeschlossen."
exit()
