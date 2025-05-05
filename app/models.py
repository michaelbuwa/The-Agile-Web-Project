from app import db

# The table to store a list of users and their details
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True)
    birth_year = db.Column(db.Integer)
    nationality = db.Column(db.String(100))
    colour_blindness = db.Column(db.String(100))

    # Relationship to Results
    results = db.relationship('Result', backref='user', cascade="all, delete-orphan", lazy=True)

# The table of each result everyone gets
class Result(db.Model):
    __tablename__ = 'results'

    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    colour = db.Column(db.String(20), nullable=False)  # storing as "255,255,255"
    distance = db.Column(db.Float, nullable=False)
    correct = db.Column(db.Boolean, nullable=False)