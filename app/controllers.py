from app.models import User
from app import db

def try_to_login_user(username, password, registering):
    user = User.query.filter_by(username=username).first()
    if registering:
        if user:
            return f"User {username} already exists"
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user
    else:
        if not user:
            return 'User does not exist'
        elif not user.check_password(password):
            return 'Wrong password'
        else:
            return user