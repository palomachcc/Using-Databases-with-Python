import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'

if api_key is False:
    api_key = 42
    serviceurl = "http://py4e-data.dr-chuck.net/json?"   #esto es si usamos la API key que nos da el
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#continua=input("hasta aca es toda la intro de librerias api key y crear la base con 1 tabla")

fh = open("where.data")
count = 0
for line in fh:
    if count > 200 :
        print('Retrieved 200 locations, restart to retrieve more')
        break #esto es para que cuando llega a los 200 datos, corte
    #print("count es igual a",count,"linea", count + 1,"--->", line)
    #continua=input("hasta aca imprimio la primera linea de lo que encontro en where.data sin hacerle nada")

    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM Locations WHERE address= ?",
        (memoryview(address.encode()), ))

    #print(address.encode())
    #continua=input("arriba imprimio adress.encode()")
    try:  #toma toda la info ya guardada en la base. para no repetir
        data = cur.fetchone()[0]
        #print(data) #data es un choclo enorme...
        #continua=input("aca imprime data=cur.fetchone()[0]")
        print("Found in database ",address)
        continue
    except:
        pass

    parms = dict()
    parms["address"] = address
    #continua=input("voy a imprimir parms que es un dic qeu contiene a adress") #aparece un lugar de la lista de where.data
    #print(parms)
    if api_key is not False: parms['key'] = api_key
    #continua=input("voy a imprimir parms devuelta") # ahora tengo un adress y una key API
    #print(parms)

    url = serviceurl + urllib.parse.urlencode(parms) #escribe toda la direccion
    print('Retrieving', url)

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()  # aca tiene toda la data de la direccion "geodata"
    #continua=input("voy a imprimir uh.read().decode() que es un choclo pero el te lo resume") # ahora tengo un adress y una key API
    #print(data)

    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' ')) #word[:2]   # character from the beginning to position 2 (excluded) y .replace(,) es que reemplace el cambio de renglon por un espacio
    count = count + 1

    try:
        js = json.loads(data) #todo el choclo de data pero en codigo pyhton y en forma de dicc. para que hace esto?

    except:
        print(data)  # We print in case unicode causes an error
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') : #si pongo universidad nacional de san martin en where.data me tira zero?results
        print('==== Failure To Retrieve ====')
        print(data)
        break

    #continua=input("imprimo data.encode()")
    #print(address.encode())
    cur.execute('''INSERT INTO Locations (address, geodata)
            VALUES ( ?, ? )''', (memoryview(address.encode()), memoryview(data.encode()) ) )
    conn.commit()
    if count % 10 == 0 :
        print('Pausing for a bit...')
    #   time.sleep(5)

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")

exit=input("exit")
