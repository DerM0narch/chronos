from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import Nutzer, Buchung
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user, login_user, logout_user
from .auth import auth

views = Blueprint('views', __name__)


@views.route("/index", methods=["GET", "POST"])
def index():
    return redirect(url_for("auth.login"), user=current_user)

@views.route("/startseite", methods=["GET", "POST"])
@login_required
def startseite():
    if request.method == 'POST':
        if request.form['button_startseite'] == 'button_kommen':
            
            statusUpdate = Nutzer.query.filter_by(id=current_user.id).first()
            statusUpdate.benutzerStatus = 'anwesend'
            
            buchung = Buchung("anwesend", statusUpdate.kartennr)
            db.session.add(buchung)
            db.session.commit()
            
        elif request.form['button_startseite'] == 'button_pause':
            
            statusUpdate = Nutzer.query.filter_by(id=current_user.id).first()
            statusUpdate.benutzerStatus = 'Pause'
            
            buchung = Buchung("Pause", statusUpdate.kartennr)
            db.session.add(buchung)
            db.session.commit()
            
        elif request.form['button_startseite'] == 'button_gehen':
            statusUpdate = Nutzer.query.filter_by(id=current_user.id).first()
            statusUpdate.benutzerStatus = 'abwesend'
            
            buchung = Buchung("abwesend", statusUpdate.kartennr)
            db.session.add(buchung)
            db.session.commit()    

    return render_template('startseite.html', user=current_user)


@views.route('/nutzeranlegen', methods=["GET", "POST"])
def nutzeranlegen():
    if current_user.id != 1:
        flash("No Access", "error")
        return redirect(url_for('auth.login'))
    if request.method=="POST":
        try:
            A_nname = request.form.get('nname')
            A_vname = request.form.get('vname')
            A_email = request.form.get('email')
            A_passwort = request.form.get('passwort')
            A_kartennr = request.form.get('kartennr')

            benutzer = Nutzer(nname=A_nname, vname=A_vname, email=A_email, passwort=A_passwort, kartennr=A_kartennr)

            db.session.add(benutzer)
            db.session.commit()
        except Exception:
            flash("Es ist ein Fehler unterlaufen", category='error')
        else:
            flash("Nutzer erfolgreich erstellt", category="success")
            

    return render_template('nutzerAnlegen.html')

