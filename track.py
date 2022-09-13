import xml.etree.ElementTree as ET   #para importar codigo xml y manejarlo. https://docs.python.org/3/library/xml.etree.elementtree.html
import sqlite3  #para hablar con la base de datos de SQLite

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript() para que sirve la funcion--->https://www.pythonparatodo.com/?p=166
# Para que sirve UNIQUE --->https://www.sqlitetutorial.net/sqlite-unique-constraint/
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')


fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Library.xml'   #podria practicar sacarlo de la web. https://www.py4e.com/code3/tracks/Library.xml

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>

#el siguiente parrafo es donde busca. Arma una funcion de dos parametros.
def lookup(d, key):
    found = False
    for child in d:     #child seria cada una de las cosas que contiene cada uno de los elementos de "all"
        if found : return child.text
        if child.tag == 'key' and child.text == key :     #si en el child.tag dice key y el texto es Name o composer o album, etc. Las que dicen <key> les corresponde esas opciones: name, composer, album, artist, genre, kind, size,etc
            found = True
    return None

## NOTE: **
""" d= es el elemento "dict/dict/dict" que empezaba asi...
<key>Track ID</key>
<integer>369</integer>
<key>Name</key>
<string>Another One Bites The Dust</string>
<key>Artist</key>
<string>Queen</string>
<key>Composer</key>
<string>John Deacon</string>
<key>Album</key>"""

#The key for an object is inside the objetc. al parecer eso es algo raro
# "if var :"  --->https://stackoverflow.com/questions/20809417/what-does-if-var-mean-in-python ver archivo "boolean expressions"
#la parte que sigue..."if child.tag" tiene que ver con la libreria de xml --->https://docs.python.org/3/library/xml.etree.elementtree.html


stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
#all me da una lista de todos los elementos encontrados segun mi filtro ....dict/dict/dict ....Si lo imprimo tiene un formato asi: "Dict at ksjaksjkfkdj"
#en la estructura del archivo tengo Dict---->Dict---->Dict (recien en este "dict" esta la info de la musica)

print('Dict count:', len(all))
for entry in all:
    #para cada elemento de all, quiero que realice lo siguiente:
    if ( lookup(entry, 'Track ID') is None ) : continue    # Si la funcion no encuentra Track ID al pincipio, retorna None al toque y pasa al siguiente elemento de all
    #continue significa que vuelve a retomar el loop, en este caso pasaria al siguiente elemento. The continue keyword is used to end the current iteration in a for loop (or a while loop), and continues to the next iteration.
    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or album is None :
        continue

    print(name, artist, album, count, rating, length)

# "OR IGNORE" lo usa porque arriba aclaro que ciertos datos eran UNIQUE. Si repite ese dato, blowup
    cur.execute('''INSERT OR IGNORE INTO Artist (name)
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, len, rating, count)
        VALUES ( ?, ?, ?, ?, ? )''',
        ( name, album_id, length, rating, count ) )

    conn.commit()
