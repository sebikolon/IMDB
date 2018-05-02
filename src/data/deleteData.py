import sqlite3
from src import webscraping

def deleteData():
    # Creates or opens a file called mydb with a SQLite3 DB
    db = sqlite3.connect(webscraping.path_to_database)

    # Get a cursor object
    cursor = db.cursor()

    # Update an specific object
    cursor.execute(''' DROP TABLE actor ''')
    cursor.execute(''' DROP TABLE film ''')
    cursor.execute(''' DROP TABLE filmgenres ''')
    cursor.execute(''' DROP TABLE award ''')
    cursor.execute(''' DROP TABLE genre ''')

    db.commit()
    db.close();