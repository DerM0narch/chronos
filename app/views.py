from flask import Blueprint, render_template, request, flash
from . import db
from .models import Nutzer, Buchung

views = Blueprint('views', __name__)


@views.route("/")
def index():
    return render_template('index.html')

@views.route("/login")
def login():
    return render_template('login.html')


@views.route('/nutzeranlegen', methods=["GET", "POST"])
def nutzeranlegen():
    if request.method=="POST":
        try:
            A_nname = request.form.get('nname')
            A_vname = request.form.get('vname')
            A_kuerzel = A_nname[:4].lower() + A_vname[:3].lower()
            A_email = request.form.get('email')
            A_passwort = request.form.get('passwort')
            A_kartennr = request.form.get('kartennr')

            benutzer = Nutzer(nname=A_nname, vname=A_vname, nutzername=A_kuerzel,
                            email=A_email, passwort=A_passwort, 
                            kartennr=A_kartennr)

            db.session.add(benutzer)
            db.session.commit()
        except Exception:
            flash("Es ist ein Fehler unterlaufen", category='error')
        else:
            flash("Nutzer erfolgreich erstellt", category="success")
            

    return render_template('nutzerAnlegen.html')