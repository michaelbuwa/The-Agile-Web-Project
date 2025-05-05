from flask import render_template
from flask import jsonify
from app import application 

@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html', title='Colour Mania', include_google_fonts=True, include_bootstrap=True)

@application.route('/sign-up')
def sign_up():
    return render_template('sign-up.html', title='Sign Up', include_bootstrap=True)

@application.route('/upload')
def upload():
    return render_template('upload.html', title='Colour Differentiation Test', include_navbar=True, body_class='upload-page')

@application.route('/visualise')
def visualise():
    return render_template('visualise.html', title='Data Visualisation', include_navbar=True)

@application.route('/share')
def share():
    return render_template('share.html', title='Share', include_navbar=True, include_bootstrap=True)


@application.route('/api/stats')
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