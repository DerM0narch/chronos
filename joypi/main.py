from mfrc522 import SimpleMFRC522
import RPi.GPIO as gpio
import sqlite3 as sql
from sqlite3 import Error
from datetime import datetime


DB_NAME = "chronos.db"
DB_FILE = F'../app/{DB_NAME}'


reader = SimpleMFRC522()

def RFIDread():
    """ read the card id and add a 'Buchung' according to the last status of the"""    
    con = create_connection(DB_FILE)
    gpio.setwarnings(False)
    
    while True:
        try:
            kartenscan = str(reader.read())
            kartenid = str(kartenscan[0])
            print(kartenid)
            print(type(kartenid))
        finally:
            gpio.cleanup()
        
        with con:
            
            cur = con.cursor()
            
            cur.execute(F"SELECT benutzerStatus FROM Nutzer WHERE kartennr={kartenid}")
            result = cur.fetchone()
            print(result)
            if result == "abwesend" or result == "in Pause":
                cur.execute(F"INSERT INTO Buchung (buchungArt, buchungdate, n_kartennr) VALUES ('anwesend', {str(datetime.now())}, {kartenid})")
                con.commit()
            elif result == "anwesend":
                cur.execute(F"INSERT INTO Buchung (buchungArt, buchungdate, n_kartennr) VALUES ('abwesend', {datetime.now()}, {kartenid})")
                con.commit()
        

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sql.connect(db_file)
    except Error as e:
        print(e)

    return conn
    
if __name__ == "__main__":
    RFIDread()