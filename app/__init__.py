from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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
    from .models import Nutzer
    
    create_database(app)
    
    # Login Managing
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return Nutzer.query.get(int(id))
    
    return app
    

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')