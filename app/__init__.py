"""
Template from labs to be altered later

from flask import Flask
app = Flask(__name__)

from app import routes
"""

"""
Database Flask integration
"""
from flask import flask
from flask import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)

from app import routes, models