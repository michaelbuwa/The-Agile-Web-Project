from flask import render_template, flash, redirect, url_for, request
from flask import jsonify
from sqlalchemy import func
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import LoginForm,SignUpForm
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

def rgb_string_to_tuple(rgb_str):
    """Converts 'rgb(123, 45, 67)' to (123, 45, 67)"""
    return tuple(map(int, rgb_str.strip("rgb() ").split(",")))

@app.route('/api/update_match', methods=['POST'])
@login_required
def update_match():
    data = request.get_json()
    is_correct = data.get('is_correct', False)
    correct_color_str = data.get('correct_color')
    selected_color_str = data.get('selected_color')

    # Update the user's correct_matches count if the match is correct
    if is_correct:
        current_user.correct_matches += 1
        db.session.commit()

    correct_color_tpl = rgb_string_to_tuple(correct_color_str)
    selected_color_tpl = rgb_string_to_tuple(selected_color_str)

    #Calculate distance between the two colors
    distance = None
    if not is_correct:
        cr, cg, cb = correct_color_tpl[0], correct_color_tpl[1], correct_color_tpl[2]
        sr, sg, sb = selected_color_tpl[0], selected_color_tpl[1], selected_color_tpl[2]
        distance = math.sqrt((cr - sr)**2 + (cg - sg)**2 + (cb - sb)**2)
    
    result = GameResult(
        user_id=current_user.id,
        correct_color=correct_color_str,
        selected_color=selected_color_str,
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
    return render_template('visualise.html', title='Data Visualisation', include_navbar=True, include_google_fonts=True, correct_matches=user.correct_matches)


@app.route('/share')
@login_required
def share():
    return render_template('share.html', title='Share', include_navbar=True, include_bootstrap=True)


@app.route('/api/search_users')
@login_required
def search_users():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify([])

    matching_users = User.query.filter(
        User.username.ilike(f'%{query}%'),
        User.username != current_user.username
    ).limit(10).all()

    return jsonify([user.username for user in matching_users])

@app.route('/api/unlocked', methods=['GET'])
@login_required
def get_stats():
    user_id = current_user.id

    # --- Get unlocked (used) colors for this user ---
    colors = (
    db.session.query(GameResult.correct_color)
    .filter_by(user_id=user_id)
    .filter(GameResult.is_correct == True)
    .distinct()
    .all()
)
    
    # # Extract actual colors
    # colors = Color.query.filter(GameResult..in_(color_ids)).all()
    print(colors)
    unlocked_colors = []
    for c in colors:
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


@app.route('/api/incorrect', methods=['GET'])
@login_required
def get_incorrect():
    user_id = current_user.id

    results = (
        db.session.query(GameResult)
        .filter_by(user_id=user_id)
        .filter(GameResult.is_correct == False)
        .all()
    )

    colors = []
    for result in results:
        try:
            correct_color = result.correct_color
            selected_color = result.selected_color
            distance = result.euclidean_distance

            r1, g1, b1 = map(int, correct_color.strip('rgb() ').split(','))
            r2, g2, b2 = map(int, selected_color.strip('rgb() ').split(','))

            colors.append({
                'correct': {'r': r1, 'g': g1, 'b': b1},
                'selected': {'r': r2, 'g': g2, 'b': b2},
                'distance': distance
            })

        except Exception as e:
            print(f"Error parsing color: {e}")

    return jsonify({'tricky_colors': colors})


@app.route('/api/distance')
@login_required
def get_dist():
    pass