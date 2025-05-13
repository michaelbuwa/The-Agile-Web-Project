from flask import render_template, flash, redirect, url_for, request
from flask import jsonify
from sqlalchemy import func
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import LoginForm
from app.models import User, GameResult, Friendship
from app import app,db
import math

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        registering = form.register.data
        
        user = User.query.filter_by(username=username).first()
        if registering:
            if user:
                flash('Username {username} already exists','error')
            else:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit() #Save the new user to the database,ensures database is consistent
                login_user(user)
                return redirect(url_for('upload'))
        if not user:
            flash('Username does not exist','error')
        elif not user.check_password(password):
            flash('Incorrect password','error')
        else:
            login_user(user)
            return redirect(url_for('upload'))
    return render_template('index.html', title='Colour Mania', include_google_fonts=True, include_bootstrap=True,form=form)

@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html', title='Sign Up', include_bootstrap=True)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html', title='Colour Differentiation Test', include_navbar=True, body_class='upload-page')

def rgb_string_to_tuple(rgb_str):
    """Converts 'rgb(123, 45, 67)' to (123, 45, 67)"""
    return tuple(map(int, rgb_str.strip("rgb() ").split(",")))



@app.route('/api/update_match', methods=['POST'])
@login_required
def update_match():
    data = request.get_json()
    is_correct = data.get('is_correct', False)
    correct_colour_str = data.get('correct_color')
    selected_colour_str = data.get('selected_color')

    # Update the user's correct_matches count if the match is correct
    if is_correct:
        current_user.correct_matches += 1
        db.session.commit()

    correct_colour_tpl = rgb_string_to_tuple(correct_colour_str)
    selected_colour_tpl = rgb_string_to_tuple(selected_colour_str)

    #Calculate distance between the two colours
    distance = None
    if not is_correct:
        cr, cg, cb = correct_colour_tpl[0], correct_colour_tpl[1], correct_colour_tpl[2]
        sr, sg, sb = selected_colour_tpl[0], selected_colour_tpl[1], selected_colour_tpl[2]
        distance = math.sqrt((cr - sr)**2 + (cg - sg)**2 + (cb - sb)**2)
    
    result = GameResult(
        user_id=current_user.id,
        correct_colour=correct_colour_str,
        selected_colour=selected_colour_str,
        is_correct=is_correct,
        euclidean_distance=distance
    )
    db.session.add(result)
    db.session.commit()

    return jsonify({'success': True, 'correct_matches': current_user.correct_matches})

@app.route('/visualise')
@login_required
def visualise():
    user = User.query.get(current_user.id)
    return render_template('visualise.html', title='Data Visualisation', include_navbar=True, correct_matches=user.correct_matches)


@app.route('/share')
@login_required
def share():
    return render_template('share.html', title='Share', include_navbar=True, include_bootstrap=True)


@app.route('/api/unlocked')
@login_required
def get_stats():
    user_id = current_user.id

    # --- Get unlocked (used) colours for this user ---
    colours = (
    db.session.query(GameResult.correct_colour)
    .filter_by(user_id=user_id)
    .filter(GameResult.is_correct == True)
    .distinct()
    .all()
)
    
    # # Extract actual colours
    # colours = Colour.query.filter(GameResult..in_(colour_ids)).all()
    print(colours)
    unlocked_colors = []
    for c in colours:
        rgb_str = c[0]  # Get the string like 'rgb(149, 168, 246)'
        try:
            # Strip 'rgb(' and ')' and split into r, g, b
            r, g, b = map(int, rgb_str.strip('rgb() ').split(','))
            unlocked_colors.append({'r': r, 'g': g, 'b': b})
        except Exception as e:
            print(f"Error parsing color {rgb_str}: {e}")
        
    return jsonify({
        'unlocked_colors': unlocked_colors,
    })

# @app.route('/api/incorrect')
# @login_required
# def get_stats():
#     user_id = current_user.id

#     # --- Get unlocked (used) colours for this user ---
#     colours = db.session.query(GameResult.correct_colour).filter_by(user_id=user_id).distinct().all()
    
#     # # Extract actual colours
#     # colours = Colour.query.filter(GameResult..in_(colour_ids)).all()
#     print(colours)
#     unlocked_colors = []
#     for c in colours:
#         rgb_str = c[0]  # Get the string like 'rgb(149, 168, 246)'
#         try:
#             # Strip 'rgb(' and ')' and split into r, g, b
#             r, g, b = map(int, rgb_str.strip('rgb() ').split(','))
#             unlocked_colors.append({'r': r, 'g': g, 'b': b})
#         except Exception as e:
#             print(f"Error parsing color {rgb_str}: {e}")
        
#     return jsonify({
#         'unlocked_colors': unlocked_colors,
#     })

# @app.route('/api/distance')
# @login_required
# def get_stats():
#     user_id = current_user.id

#     # --- Get unlocked (used) colours for this user ---
#     colours = db.session.query(GameResult.correct_colour).filter_by(user_id=user_id).distinct().all()
    
#     # # Extract actual colours
#     # colours = Colour.query.filter(GameResult..in_(colour_ids)).all()
#     print(colours)
#     unlocked_colors = []
#     for c in colours:
#         rgb_str = c[0]  # Get the string like 'rgb(149, 168, 246)'
#         try:
#             # Strip 'rgb(' and ')' and split into r, g, b
#             r, g, b = map(int, rgb_str.strip('rgb() ').split(','))
#             unlocked_colors.append({'r': r, 'g': g, 'b': b})
#         except Exception as e:
#             print(f"Error parsing color {rgb_str}: {e}")
        
#     return jsonify({
#         'unlocked_colors': unlocked_colors,
#     })