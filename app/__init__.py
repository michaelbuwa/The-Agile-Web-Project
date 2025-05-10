"""
Template from labs to be altered later

from flask import Flask
app = Flask(__name__)

from app import routes
"""

"""
Database Flask integration
"""
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.extensions import login

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models