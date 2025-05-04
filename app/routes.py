from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Colour Mania', include_google_fonts=True, include_bootstrap=True)
@app.route('/sign-up')
def sign_up():
	return render_template('sign-up.html', title='Sign Up', include_bootstrap=True)
@app.route('/upload')
def upload():
	return render_template('upload.html', title='Colour Differentiation Test', include_navbar=True, body_class='upload-page')
@app.route('/visualise')
def visualise():
	return render_template('visualise.html', title='Data Visualisation', include_navbar=True)
@app.route('/share')
def share():
	return render_template('share.html', title='Share', include_navbar=True, include_bootstrap=True)
