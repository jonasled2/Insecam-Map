with open ("index.html", 'w') as out:
  import requests
  out.write('   <!DOCTYPE html>\n   <html>\n   <head>\n     <meta http-equiv="content-type" content="text/html; charset=ANSI" />\n     <title>Insecam Map</title>\n     <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBYZ2z4zcTrdDt6r5TpB4aiI1EkLS2xRms&callback=initMap"\n      type="text/javascript"></script>\n   </head>\n   <body>\n     <div id="map" style="width: 1500px; height: 1000px;"></div>\n\n     <script type="text/javascript">\n       var locations = [')
  url = []
  r = requests.get('http://www.insecam.org/en/bycountry/DE/?page=1', headers={'user-agent': 'mozilla'})
  seiten = r.text.split('pagenavigator("?page=", ')[1].split(",")[0]
  print seiten
  for i in range(1, int(seiten) + 1):
    r = requests.get('http://www.insecam.org/en/bycountry/DE/?page=' + str(i), headers={'user-agent': 'mozilla'})
    print i
    for x in range (0, r.text.count('/en/view/')):
      url.append(str(r.text.split('/en/view/')[x+1].split('/"')[0]))


  print "fertig"
  print str(len(url))
  i = 0
  for i in range(0, len(url)):
    print i
    r = requests.get('http://www.insecam.org/en/view/' + url[i], headers={'user-agent': 'mozilla'})
    lat = r.text.split("Latitude:")[1].split('">\n')[1].split("\n<")[0]
    lon = r.text.split("Longitude:")[1].split('">\n')[1].split("\n<")[0]
    city = r.text.split('View camera')[1].split(', ')[1].split('</h1>')[0]
    print city
    if (i == len(url) - 1):
      out.write('        ["' + str(city) + '", ' + str(lat) + ', ' + str(lon) + ', "http://www.insecam.org/en/view/' + str(url[i]) + '"]];\n')
    if (i != len(url) - 1):
      out.write('        ["' + str(city) + '", ' + str(lat) + ', ' + str(lon) + ', "http://www.insecam.org/en/view/' + str(url[i]) + '"],\n')
  print "fertig"
  out.write('var map = new google.maps.Map(document.getElementById("map"), {\n  zoom: 5,\n center: new google.maps.LatLng(51.54376, 9.910419999999931),\n mapTypeId: google.maps.MapTypeId.ROADMAP\n});\n\nvar infowindow = new google.maps.InfoWindow();\n\nvar marker, i;\n\nfor (i = 0; i < locations.length; i++) {\n  marker = new google.maps.Marker({\n   position: new google.maps.LatLng(locations[i][1], locations[i][2]),\n   map: map,\n   url: locations[i][3]\n  });\n\n google.maps.event.addListener(marker, "mouseover", (function(marker, i) {\n   return function() {\n     infowindow.setContent(locations[i][0]);\n     infowindow.open(map, marker);\n   }\n })(marker, i));\n\n      google.maps.event.addListener(marker, "click", (function(marker, i) {\n   return function() {\n     infowindow.setContent(locations[i][0]);\n     infowindow.open(map, marker);\n     window.location.href = this.url;\n   }\n })(marker, i));\n\n    }\n\n     </script>\n   </body>\n   </html>')
