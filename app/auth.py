from . import db
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from .models import Nutzer

auth = Blueprint('auth', __name__)


@auth.route("/login")
def login():
    if request.method == 'POST':
        username = request.form.get('user')
        passwort = request.form.get('password')
        
        nutzer = Nutzer.query.filter_by(nutzername=username).first()
        
        if nutzer:
            if nutzer.passwort == passwort:
                flash("Logged in", "succesful")
                login_user(nutzer, remember=True)
                return redirect(url_for('views.startseite'))

    return render_template('login.html', nutzer=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))