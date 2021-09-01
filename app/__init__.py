from flask import Flask
from app import db
from app import routes

app = Flask(__name__)



db.create_all()
app.run(debug=True)