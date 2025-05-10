from app import db

# The table to store a list of users and their details
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    correct_matches = db.Column(db.Integer, default=0)

    game_results = db.relationship('GameResult', backref='user', lazy=True)
    # One-to-many: this user "owns" these friendship entries
    friendships = db.relationship('Friendship', backref='owner', lazy=True)

class Colour(db.Model):
    __tablename__ = 'colours'
    id = db.Column(db.Integer, primary_key=True)
    rgb_val = db.Column(db.String(20), nullable=False) # e.g., "rgb(255, 100, 30)"

# The table of each result everyone gets
class GameResult(db.Model):
    __tablename__ = 'game_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    correct_colour_id = db.Column(db.Integer, db.ForeignKey('colours.id'), nullable=False)
    selected_colour_id = db.Column(db.Integer, db.ForeignKey('colours.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    euclidean_distance = db.Column(db.Float) # Null for correct answers

class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # owner
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # the added friend