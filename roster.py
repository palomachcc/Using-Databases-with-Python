import json
import sqlite3

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()   #como un file handle pero en este caso para el servidor de la base de datos

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

#la tabla member tiene dos FOREIGN KEY
#(role= 1 si es profe 0 si es estudiante)
#fijate que puso : PRIMARY KEY "compuesta"(user_id, course_id) . la primary key es la combinacion de dos columnas

fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data.json'   #https://www.py4e.com/code3/roster/roster_data_sample.json

continua1=input("encontro el archivo OK")
# [
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

str_data = open(fname).read()
continua2=input("abre el archivo OK")

json_data = json.loads(str_data) #json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary.
continua2=input("parse the file OK")

for entry in json_data:      # ENTRE SERA ALGO DEL ESTILO [ "Charley", "si110", 1 ],

    name = entry[0]    #"Charley"
    title = entry[1]   #"si110"
    role= entry[2]     #1
    #print((name, title, role))

    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]    #el cero es porque primero esta la columna de id y luego el nombre
#OR IGNORE es por si llega a explotar, por ejemplo si ingreass el mismo nombre dos veces
    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]
#.fetchone() retrieves the next row of a query result set and returns a tuple, or None if no more rows are available. By default, the returned tuple consists of data returned by the MySQL server, converted to Python objects.
    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        ( user_id, course_id, role ) )

    conn.commit()

exit=input("press enter to exit")
