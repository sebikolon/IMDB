#import sqlite3
from src import webscraping as ws

def dataconnect():
    # Enable foreign key support
    ws.cursor.execute('''PRAGMA foreign_keys = 1''')
    ws.db.commit()

    ws.cursor.execute('''
    CREATE TABLE IF NOT EXISTS actor (
        'ActorID'       INTEGER UNIQUE,
        `Surname`	    TEXT,
        `Prename`	    TEXT,
        `Date_of_birth`	date,
        `Origin`	    TEXT,
        `Photo_link`	TEXT,
        `Description`	TEXT,
        PRIMARY KEY(Surname,Prename)
    ) ''')
    ws.db.commit()

    ws.cursor.execute('''
        CREATE TABLE if not exists film
            (
            'FilmID'    INTEGER UNIQUE,
            'ActorID'   INTEGER,
            `Title`	    TEXT,
            `Year`	    INTEGER,
            `Rating`	FLOAT,
            PRIMARY KEY(Title,Year),
            FOREIGN KEY(`ActorID`) REFERENCES `actor`(`ActorID`) ON UPDATE CASCADE ON DELETE SET NULL
	)
        ''')
    ws.db.commit()

    ws.cursor.execute('''
           CREATE TABLE if not exists genre
            (
            GenreID INTEGER UNIQUE,
            Description TEXT,
			PRIMARY KEY(Description))
            ''')
    ws.db.commit()

    ws.cursor.execute('''
               CREATE TABLE if not exists filmgenres
                ('FilmID'    INTEGER,
                 'GenreID'    INTEGER,
                  FOREIGN KEY(`FilmID`) REFERENCES `film`(`FilmID`) ON DELETE CASCADE
                  FOREIGN KEY(`GenreID`) REFERENCES `genre`(`GenreID`) ON DELETE CASCADE
                )''')
    ws.db.commit()

    ws.cursor.execute('''
            CREATE TABLE if not exists award
            (
            AwardID INTEGER UNIQUE,
            `Description`	TEXT,
            'Name' TEXT,
            `Year`	INTEGER,
            `ActorID`	INTEGER,
            PRIMARY KEY(Description,Year,ActorID),
            FOREIGN KEY(`ActorID`) REFERENCES `actor`(`ActorID`) ON UPDATE CASCADE ON DELETE SET NULL
            )''')
    ws.db.commit()
