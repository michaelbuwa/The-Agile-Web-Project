from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from app.extensions import login

db = SQLAlchemy()

def create_application(config):
    application = Flask(__name__)
    application.config.from_object(config)

    from app.blueprints import blueprint
    application.register_blueprint(blueprint)

    db.init_app(application)
    login.init_app(application)

    return application