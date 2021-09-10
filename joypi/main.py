from app import DB_NAME
from mfrc522 import SimpleMFRC522
import RPi.GPIO as gpio
import sqlite3 as sql
from sqlite3 import Error

DB_NAME = "chronos.db"
DB_FILE = F'app/{DB_NAME}'


reader = SimpleMFRC522()

def RFIDread():
    con = sql.create_connection(DB_FILE)
    gpio.setwarnings(False)
    
    while True:
        try:
            kartenid = reader.read()
        finally:
            gpio.cleanup()
        
        with con:
            
            cur = con.cursor()
            
            cur.execute(F"SELECT benutzerstatus from Nutzer where kartennr={kartenid}")
            result = cur.fetchone()
            
            if result == "abwesend" or result == "in Pause":
                pass
            elif result == "anwesend":
                pass
        

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