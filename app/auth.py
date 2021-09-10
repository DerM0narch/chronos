from . import db
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from .models import Nutzer

auth = Blueprint('auth', __name__)


@auth.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.startseite", user=current_user))
    if request.method == 'POST':
        username = request.form.get('user')
        passwort = request.form.get('password')
        
        nutzer = Nutzer.query.filter_by(nutzername=username).first()
        
        if nutzer:
            if check_password_hash(nutzer.passwort, passwort):
                flash("Logged in", "succesful")
                login_user(nutzer, remember=True)
                return redirect(url_for("views.startseite", user=current_user))
            else:
                flash("Nutzername oder Passwort ist falsch", "error")
        else:
            flash("Nutzer nicht gefunden. Bitte einen Admin kontaktieren!", "error")

    return render_template('index.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))