import urllib.request, urllib.parse, urllib.error
import json
import ssl

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'
# https://developers.google.com/maps/documentation/geocoding/intro

if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else :
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    address = input('Enter location: ')
    if len(address) < 1: break                    #si apretas enter se sale. Sino sigue repitiendo el "enter location"

    parms = dict()
    parms['address'] = address       # le asigna a address: el nombre que acabo de ingresar en location

    #print("parms:",parms)            #si ingrese ann arbor por ejemplo---> parms: {"address" : "Ann Arbor"}



#The program takes the search string and constructs a URL with the search string as a properly encoded parameter
    if api_key is not False: parms['key'] = api_key

    #print("parms:",parms)  # parms: {"address" : "Ann Arbor", "key":42}
    #rint(urllib.parse.urlencode(parms)) # me devuelve ---> address=ann+arbor&key=42  . Ver https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode

    url = serviceurl + urllib.parse.urlencode(parms)  # aca lo que hace es concatenar.

#then uses urllib to retrieve the text from the Google geocoding API. Unlike a fixed web page, the data we get depends on the
#parameters we send and the geographical data stored in Google’s servers.

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()        # read, agarraba todo el texto de la web. decode porque seguro venia como UTF-8. data es ahora un pyhton unicode string
    #print('Retrieved', len(data), 'characters')
    #print("esto es lo que sale de json.loads(data):",data)
#Once we retrieve the JSON data, we parse it with the json library and do a few checks to make sure that we received good data,
#then extract the information that we are looking for.

    try:
        js = json.loads(data)           #aca es como haia con beautiful soup ponele. obtiene un diccionario
    except:
        js = None
#el codigo que obtenes es un diccionario {}. adentro tenes dos cosas -results- y -status-. status debe decir OK.
    if not js or 'status' not in js or js['status'] != 'OK':    #if not js. quiere decir que js=None, si js= json.loads(data) continua...
        print('==== Failure To Retrieve ====')   # si no dice OK o
        print(data)
        continue

    print(json.dumps(js, indent=4))  #json.dumps() function converts a Python object into a json string.indent:If indent is a non-negative integer or string, then JSON array elements and object members will be pretty-printed with that indent level. An indent level of 0, negative, or “” will only insert newlines. None (the default) selects the most compact representation. Using a positive integer indent indents that many spaces per level. If indent is a string (such as “\t”), that string is used to indent each level. Sin esto, te imprime todo un parrafo y no tipo codigo
    lat = js['results'][0]['geometry']['location']['lat']  #aca lo que hace es recorrer "el arbol".dentro de results el componente 0 y ahi geometry y location y lat
    lng = js['results'][0]['geometry']['location']['lng']
    print('lat', lat, 'lng', lng)
    location = js['results'][0]['formatted_address']
    print(location)
