from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Nutzer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nname = db.Column(db.String(50))
    vname = db.Column(db.String(50))
    nutzername = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(50))
    passwort = db.Column(db.String(50))
    kartennr = db.Column(db.String(50), unique=True)
    benutzerStatus = db.Column(db.String(10), default='abwesend')
    
    def __init__(self, nname, vname, email, passwort, kartennr):
        self.nname = nname
        self.vname = vname
        self.nutzername = nname[:4].lower() + vname[:3].lower()
        self.email = email
        self.passwort = generate_password_hash(passwort, method='sha256')
        self.kartennr = kartennr
    
    def __repr__(self):
        return f'<Nutzer {self.id} - {self.nutzername}>'
    

class Buchung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buchungArt = db.Column(db.String(10),)
    n_kartennr = db.Column(db.String(50), db.ForeignKey('nutzer.id'))
    
    def __repr__(self):
        return f'<Buchung {self.buchungArt} mit {self.n_kartennr}'
