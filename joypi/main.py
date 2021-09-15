from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import sqlite3 as sql
from sqlite3 import Error
from datetime import datetime
import time

DB_NAME = "chronos.db"
DB_FILE = F'../app/{DB_NAME}'
BUZZER_PIN = 12
LED_PIN = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

reader = SimpleMFRC522()

def RFIDread():
    """ read the card id and add a 'Buchung' according to the last status of User"""    
    con = create_connection(DB_FILE)
    GPIO.setwarnings(False)
    
    # Karte lesen
    while True:
        try:
            kartenscan, text = reader.read()
            kartenid = str(kartenscan)
            print("Kartenid: " + kartenid)
        finally:
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(LED_PIN, GPIO.OUT)
            GPIO.output(LED_PIN, GPIO.LOW) 

        # Datenbankeintrag in Buchung
        with con:
            
            cur = con.cursor()
            
            cur.execute("SELECT benutzerStatus FROM Nutzer WHERE kartennr=?", (kartenid,))
            result = str(cur.fetchone()[0])
            print("alter Status: " + result)
            if result == "abwesend" or result == "Pause":
                cur.execute("INSERT INTO Buchung (buchungArt, buchungdate, n_kartennr) VALUES ('anwesend', ?, ?)", (str(datetime.now()), kartenid))
                cur.execute("UPDATE Nutzer SET benutzerStatus='anwesend' WHERE kartennr=?", (kartenid,))
                print("neuer Status: anwesend")
                con.commit()
            elif result == "anwesend":
                cur.execute("INSERT INTO Buchung (buchungArt, buchungdate, n_kartennr) VALUES ('abwesend', ?, ?)", (str(datetime.now()), kartenid))
                cur.execute("UPDATE Nutzer SET benutzerStatus='abwesend' WHERE kartennr=?", (kartenid,))
                print("neuer Status: abwesend")
                con.commit()
        print("--------------")
        # Buzzer als Feedback
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        GPIO.output(BUZZER_PIN, GPIO.HIGH) 
        time.sleep(0.5)
        GPIO.output(BUZZER_PIN, GPIO.LOW) 
        time.sleep(3)
        GPIO.output(LED_PIN, GPIO.HIGH) 
        
        

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