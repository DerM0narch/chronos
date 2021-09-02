from flask import render_template
from app import app

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/nutzer")
def nutzer():
    return render_template('user.html')

@app.route("/uebersicht")
def uebersicht():
    return render_template('uebersicht.html')

@app.route('/nutzeranlegen')
def nutzeranlegen():
    return render_template('nutzerAnlegen.html')