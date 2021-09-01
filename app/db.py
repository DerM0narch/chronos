from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://chronos.db'
db = SQLAlchemy(app)

class Test(db.Model):
    pass