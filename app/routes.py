from flask import render_template, flash, redirect, url_for, request
from flask import jsonify
from flask_login import login_required, login_user, logout_user
from app.forms import LoginForm,SignUpForm
from app.models import User
from app import app,db

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Username does not exist','error')
        elif not user.check_password(password):
            flash('Incorrect password','error')
        else:
            login_user(user)
            return redirect(url_for('upload'))
    return render_template('index.html', title='Colour Mania', include_google_fonts=True, include_bootstrap=True,form=form)

@app.route('/sign-up',methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == "POST":
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user:
            flash(f'Username {username} already exists', 'error')
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('upload'))
    return render_template('sign-up.html', title='Sign Up', include_bootstrap=True, form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html', title='Colour Differentiation Test', include_navbar=True, body_class='upload-page')

@app.route('/visualise')
@login_required
def visualise():
    return render_template('visualise.html', title='Data Visualisation', include_navbar=True, include_google_fonts=True)

@app.route('/share')
@login_required
def share():
    return render_template('share.html', title='Share', include_navbar=True, include_bootstrap=True)


@app.route('/api/stats')
@login_required
def get_stats():
    # would use actual database query here
    unlocked_colors = [
        {'r': 255, 'g': 0, 'b': 0},
        {'r': 0, 'g': 255, 'b': 0},
        {'r': 0, 'g': 0, 'b': 255},
        # etc...
    ]

    accuracy_table = [
        {'color': 'Red', 'accuracy': 0.5},
        {'color': 'Orange', 'accuracy': 0.5},
        {'color': 'Yellow', 'accuracy': 0.55},
        {'color': 'Green', 'accuracy': 0.55},
        {'color': 'Blue', 'accuracy': 0.42},
        {'color': 'Indigo', 'accuracy': 0.67},
        {'color': 'Violet', 'accuracy': 0.07},
    ]

    return jsonify({
        'unlocked_colors': unlocked_colors,
        'accuracy_table': accuracy_table
    })