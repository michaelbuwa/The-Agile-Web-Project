from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import login 

# The table to store a list of users and their details
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True)
    birth_year = db.Column(db.Integer)
    nationality = db.Column(db.String(100))
    colour_blindness = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))

    # Relationship to Results
    results = db.relationship('Result', backref='user', cascade="all, delete-orphan", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# The table of each result everyone gets
class Result(db.Model):
    __tablename__ = 'results'

    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    colour = db.Column(db.String(20), nullable=False)  # storing as "255,255,255"
    distance = db.Column(db.Float, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)