from . import db
from flask_login import UserMixin


class Nutzer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nname = db.Column(db.String(50))
    vname = db.Column(db.String(50))
    nutzername = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(50))
    passwort = db.Column(db.String(50))
    kartennr = db.Column(db.String(50), unique=True)
    benutzerStatus = db.Column(db.String(10), default='abwesend')
    

class Buchung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buchungArt = db.Column(db.String(10),)
    n_kartennr = db.Column(db.String(50), db.ForeignKey('nutzer.id'))
