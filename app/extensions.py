from flask_login import LoginManager

login = LoginManager()
login.login_view = 'login' # Redirect to login page if not logged in
