from flask import Flask, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy, event
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from os import path
import os

db = SQLAlchemy()
DB_NAME = "chronos.db"


def create_app():
    
    # App Setup
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Communism"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    # Routes Blueprints
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    # Database
    from .models import Nutzer, Buchung
    
    create_database(app)
    
    # Login Managing
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return Nutzer.query.get(int(id))
    
    # Admin Panel
    class NutzerView(ModelView):
        can_create = False
        can_edit = False
        column_display_pk = True
        column_list = ['id', 'nname', 'vname','nutzername', 'email', 'kartennr']
        column_labels = dict(id='ID', nname='Nachname', vname='Vorname', nutzername='Kuerzel', email='E-Mail', kartennr='Kartennummer')
        
    admin = Admin(app)
    admin.add_view(NutzerView(Nutzer, db.session))
    admin.add_view(ModelView(Buchung, db.session))
    
    return app
    

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')