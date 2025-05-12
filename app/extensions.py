from flask_login import LoginManager

login = LoginManager()
login.login_view = 'index' # Redirect to sign_up page if not logged in

