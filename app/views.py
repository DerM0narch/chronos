from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import Nutzer, Buchung
from werkzeug.security import generate_password_hash, check_password_hash
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
        statusUpdate = Nutzer.query.filter_by(id=current_user.id).first()

        if request.form['button_startseite'] == 'button_kommen':
            
            statusUpdate.benutzerStatus = 'anwesend'
            
            buchung = Buchung("anwesend", statusUpdate.kartennr)
            db.session.add(buchung)
            db.session.commit()
            
        elif request.form['button_startseite'] == 'button_pause':
            
            statusUpdate.benutzerStatus = 'Pause'
            
            buchung = Buchung("Pause", statusUpdate.kartennr)
            db.session.add(buchung)
            db.session.commit()
            
        elif request.form['button_startseite'] == 'button_gehen':
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

@views.route('/meinprofil', methods=["GET", "POST"])
def meinProfil():
    #altes Passwort prüfen
    if request.method == 'POST':
        passwort = request.form.get('altes_passwort')
        neues_passwort_1 = request.form.get('neues_passwort_1')
        neues_passwort_2 = request.form.get('neues_passwort_2')
        nutzer = Nutzer.query.filter_by(id=current_user.id).first()
        
        if nutzer:
            if check_password_hash(nutzer.passwort, passwort):
                if neues_passwort_1 == neues_passwort_2:
                    try:
                        nutzer.passwort = generate_password_hash(neues_passwort_1, method='sha256')
                        db.session.commit()
                        flash("Ändern erfolgreich!", "succsses")
                    except Exception:
                        flash("Fehler unterlaufen", "error")
                else:
                    flash("Neue Passwörter sind nicht identtisch", "error")
            else:
                flash("Altes Passwort falsch", "error")

    return render_template('meinProfil.html', user=current_user)


