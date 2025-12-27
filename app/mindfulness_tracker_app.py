# By Frances Belleza
# Function: This file is like main()
#              it defines my routes & logic

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, date
from app.models import User, CheckIn, Practice, JournalPrompt
from app import db
from app.ai_service import generate_practice_and_prompt, get_fallback_content, generate_audio

def initial_routes(app):
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
                # ----- TODO: add validation (unique, email format, length) ----
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            flash('Login failed. Check your email and password.', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))

    @app.route('/check-in', methods=['GET', 'POST'])
    @login_required
    def check_in():
        # Check if user already checked in today
        today = date.today()
        existing_checkin = CheckIn.query.filter(
            CheckIn.user_id == current_user.id,
            db.func.date(CheckIn.created_at) == today
        ).first()

        if existing_checkin and request.method == 'GET':
            return redirect(url_for('already_checked_in'))

        if request.method == 'POST':
            mood = request.form.get('mood')
            body_feeling = request.form.get('body_feeling', '').strip()

            # Create new check-in
            checkin = CheckIn(
                user_id=current_user.id,
                mood=mood,
                body_feeling=body_feeling if body_feeling else None
            )
            db.session.add(checkin)
            db.session.commit()

            flash(f'Check-in saved! You\'re feeling {mood.lower()} today.', 'success')
            return redirect(url_for('practice'))

        return render_template('check_in.html')

    @app.route('/already-checked-in')
    @login_required
    def already_checked_in():
        return render_template('already_checked_in.html')

    @app.route('/practice')
    @login_required
    def practice():
        # Get user's most recent check-in from today
        today = date.today()
        latest_checkin = CheckIn.query.filter(
            CheckIn.user_id == current_user.id,
            db.func.date(CheckIn.created_at) == today
        ).first()

        # If no check-in today, redirect to check-in page
        if not latest_checkin:
            flash('Please complete your daily check-in first.', 'info')
            return redirect(url_for('check_in'))

        # Check if practice already exists for this check-in
        existing_practice = Practice.query.filter_by(checkin_id=latest_checkin.id).first()
        existing_prompt = JournalPrompt.query.filter_by(checkin_id=latest_checkin.id).first()

        # If practice already exists, display it
        if existing_practice and existing_prompt:
            return render_template('practice.html',
                                   practice=existing_practice,
                                   journal_prompt=existing_prompt)

        # Generate new AI content
        ai_result = generate_practice_and_prompt(
            mood=latest_checkin.mood,
            body_feeling=latest_checkin.body_feeling
        )

        # If AI fails, use fallback content
        if not ai_result:
            flash('Using fallback practice (AI service unavailable)', 'warning')
            ai_result = get_fallback_content(latest_checkin.mood)

        # Save practice to database
        practice_obj = Practice(
            checkin_id=latest_checkin.id,
            title=ai_result['practice']['title'],
            description=ai_result['practice']['description'],
            practice_type=ai_result['practice']['type']
        )
        db.session.add(practice_obj)

        # Save journal prompt to database
        prompt_obj = JournalPrompt(
            checkin_id=latest_checkin.id,
            prompt_text=ai_result['journal_prompt']
        )
        db.session.add(prompt_obj)

        db.session.commit()

        # Generate natural AI audio for the practice (mood-specific voice)
        audio_filename = generate_audio(
            ai_result['practice']['description'],
            practice_obj.id,
            latest_checkin.mood  # Pass mood to select appropriate voice
        )
        if audio_filename:
            practice_obj.audio_file = audio_filename
            db.session.commit()

        return render_template('practice.html',
                               practice=practice_obj,
                               journal_prompt=prompt_obj)

    @app.route('/')
    def index():
        return render_template('index.html')