#Database Flask integration
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.extensions import login
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

load_dotenv()  # this will load variables from a .env file if present

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app) # CSRF protection
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch = True)
login.init_app(app)

from app import routes, models