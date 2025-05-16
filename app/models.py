from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import login 

# The table to store a list of users and their details
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    correct_matches = db.Column(db.Integer, default=0)

    game_results = db.relationship('GameResult', backref='user', lazy=True)
    # One-to-many: this user "owns" these friendship entries
    # Sent friendships: this user sent the request
    sent_friendships = db.relationship(
        'Friendship',
        foreign_keys='Friendship.user_id',
        backref='requester',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # Received friendships: this user received the request
    received_friendships = db.relationship(
        'Friendship',
        foreign_keys='Friendship.friend_id',
        backref='recipient',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)


@login.user_loader
def load_user(id):
    return User.query.get(id)

# The table of each result everyone gets
class GameResult(db.Model, UserMixin):
    __tablename__ = 'game_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    correct_color= db.Column(db.String(20), nullable=False)
    selected_color= db.Column(db.String(20), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    euclidean_distance = db.Column(db.Float) # Null for correct answers

class Friendship(db.Model, UserMixin):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # owner
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # the added friend

    user = db.relationship('User', foreign_keys=[user_id])
    friend = db.relationship('User', foreign_keys=[friend_id])