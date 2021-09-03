from mfrc522 import SimpleMFRC522
import RPi.GPIO as gpio

reader = SimpleMFRC522()

def RFIDread():
    try:
        id = reader.read()
    finally:
        gpio.cleanup()
        return id
    