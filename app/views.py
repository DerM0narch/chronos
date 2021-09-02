from flask import Blueprint, render_template
from . import db

views = Blueprint('views', __name__)


@views.route("/")
def index():
    return render_template('index.html')

@views.route("/nutzer")
def nutzer():
    return render_template('user.html')

@views.route("/uebersicht")
def uebersicht():
    return render_template('uebersicht.html')

@views.route('/nutzeranlegen')
def nutzeranlegen():
    return render_template('nutzerAnlegen.html')