from mfrc522 import SimpleMFRC522
import RPi.GPIO as gpio

import sys
sys.path.append("..")
from app import db
from app.models import Nutzer, Buchung


reader = SimpleMFRC522()

def RFIDread():
    GPIO.setwarnings(False)
    while True:
        try:
            kartenid = reader.read()
        finally:
            gpio.cleanup()
        
        rfUser = Nutzer.query.filter_by(kartennr=kartenid).first()
        
        if rfUser.benutzerStatus == "anwesend":
            rfUser.benutzerStatus = 'abwesend'
            
            buchung = Buchung("gehen", rfUser.kartennr)
            db.session.add(buchung)
            db.session.commit()
        elif  rfUser.benutzerStatus == "abwesend" or rfUser.benutzerStatus == "in Pause":
            rfUser.benutzerStatus = 'anwesend'
            
            buchung = Buchung("kommen", rfUser.kartennr)
            db.session.add(buchung)
            db.session.commit()
    
    
if __name__ == "__main__":
    RFIDread()