# By Frances Belleza
# Function: This file is like main()
#              it defines my routes & logic

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, date
from app.models import User, CheckIn, Practice, JournalEntry, PracticeFeedback
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
        today = date.today()

        # Check for existing morning and night check-ins
        morning_checkin = CheckIn.query.filter(
            CheckIn.user_id == current_user.id,
            db.func.date(CheckIn.created_at) == today,
            CheckIn.time_of_day == 'Morning'
        ).first()

        night_checkin = CheckIn.query.filter(
            CheckIn.user_id == current_user.id,
            db.func.date(CheckIn.created_at) == today,
            CheckIn.time_of_day == 'Night'
        ).first()

        if request.method == 'POST':
            time_of_day = request.form.get('time_of_day')
            mood = request.form.get('mood')
            body_feeling = request.form.get('body_feeling', '').strip()

            # Check if user already has a check-in for this time of day
            if time_of_day == 'Morning' and morning_checkin:
                flash('You\'ve already completed your morning check-in today.', 'info')
                return redirect(url_for('already_checked_in'))
            if time_of_day == 'Night' and night_checkin:
                flash('You\'ve already completed your night check-in today.', 'info')
                return redirect(url_for('already_checked_in'))

            # Create new check-in
            checkin = CheckIn(
                user_id=current_user.id,
                mood=mood,
                body_feeling=body_feeling if body_feeling else None,
                time_of_day=time_of_day
            )
            db.session.add(checkin)
            db.session.commit()

            flash(f'{time_of_day} check-in saved! You\'re feeling {mood.lower()}.', 'success')
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
        ).order_by(CheckIn.created_at.desc()).first()

        # If no check-in today, redirect to check-in page
        if not latest_checkin:
            flash('Please complete your daily check-in first.', 'info')
            return redirect(url_for('check_in'))

        # Check if practice already exists for this check-in
        existing_practice = Practice.query.filter_by(checkin_id=latest_checkin.id).first()

        # If practice already exists, display it
        if existing_practice:
            return render_template('practice.html',
                                   practice=existing_practice)

        # Generate new AI content with time_of_day context
        ai_result = generate_practice_and_prompt(
            mood=latest_checkin.mood,
            body_feeling=latest_checkin.body_feeling,
            time_of_day=latest_checkin.time_of_day
        )

        # If AI fails, use fallback content
        if not ai_result:
            flash('Using fallback practice (AI service unavailable)', 'warning')
            ai_result = get_fallback_content(latest_checkin.mood)

        # Save practice (including journal prompt) to database
        practice_obj = Practice(
            checkin_id=latest_checkin.id,
            title=ai_result['practice']['title'],
            description=ai_result['practice']['description'],
            practice_type=ai_result['practice']['type'],
            journal_prompt=ai_result['journal_prompt']
        )
        db.session.add(practice_obj)
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
                               practice=practice_obj)

    @app.route('/reflect', methods=['GET', 'POST'])
    @login_required
    def reflect():
        # Get user's most recent check-in from today
        today = date.today()
        latest_checkin = CheckIn.query.filter(
            CheckIn.user_id == current_user.id,
            db.func.date(CheckIn.created_at) == today
        ).order_by(CheckIn.created_at.desc()).first()

        # If no check-in today, redirect to check-in page
        if not latest_checkin:
            flash('Please complete your daily check-in first.', 'info')
            return redirect(url_for('check_in'))

        # Get the practice (which contains the journal prompt)
        practice = Practice.query.filter_by(checkin_id=latest_checkin.id).first()
        if not practice:
            flash('Practice not found. Please complete your practice first.', 'warning')
            return redirect(url_for('practice'))

        if request.method == 'POST':
            entry_text = request.form.get('entry_text', '').strip()

            if not entry_text:
                flash('Please write or speak your journal entry before saving.', 'warning')
                return render_template('reflect.html', practice=practice)

            # Get time-specific responses
            intention_for_day = request.form.get('intention_for_day', '').strip() if latest_checkin.time_of_day == 'Morning' else None
            self_care_today = request.form.get('self_care_today', '').strip() if latest_checkin.time_of_day == 'Night' else None
            goal_for_tomorrow = request.form.get('goal_for_tomorrow', '').strip() if latest_checkin.time_of_day == 'Night' else None

            # Check if journal entry already exists for this check-in
            existing_entry = JournalEntry.query.filter_by(checkin_id=latest_checkin.id).first()

            if existing_entry:
                # Update existing entry
                existing_entry.entry_text = entry_text
                existing_entry.intention_for_day = intention_for_day
                existing_entry.self_care_today = self_care_today
                existing_entry.goal_for_tomorrow = goal_for_tomorrow
                flash('Journal entry updated successfully!', 'success')
            else:
                # Create new journal entry
                journal_entry = JournalEntry(
                    checkin_id=latest_checkin.id,
                    user_id=current_user.id,
                    entry_text=entry_text,
                    intention_for_day=intention_for_day,
                    self_care_today=self_care_today,
                    goal_for_tomorrow=goal_for_tomorrow
                )
                db.session.add(journal_entry)
                flash('Journal entry saved successfully!', 'success')

            db.session.commit()
            return redirect(url_for('feedback'))

        # Check if there's already an entry to display
        existing_entry = JournalEntry.query.filter_by(checkin_id=latest_checkin.id).first()

        return render_template('reflect.html',
                               practice=practice,
                               existing_entry=existing_entry)

    @app.route('/feedback', methods=['GET', 'POST'])
    @login_required
    def feedback():
        # Get user's most recent check-in from today
        today = date.today()
        latest_checkin = CheckIn.query.filter(
            CheckIn.user_id == current_user.id,
            db.func.date(CheckIn.created_at) == today
        ).order_by(CheckIn.created_at.desc()).first()

        # If no check-in today, redirect to check-in page
        if not latest_checkin:
            flash('Please complete your daily check-in first.', 'info')
            return redirect(url_for('check_in'))

        # Get the practice for this check-in
        practice = Practice.query.filter_by(checkin_id=latest_checkin.id).first()
        if not practice:
            flash('Practice not found. Please complete your practice first.', 'warning')
            return redirect(url_for('practice'))

        if request.method == 'POST':
            rating = request.form.get('rating')
            helped = request.form.get('helped')
            pacing = request.form.get('pacing')

            if not rating:
                flash('Please select a rating before continuing.', 'warning')
                return render_template('feedback.html', practice=practice)

            # Convert helped to boolean
            helped_bool = helped == 'yes' if helped else None

            # Check if feedback already exists for this practice
            existing_feedback = PracticeFeedback.query.filter_by(practice_id=practice.id).first()

            if existing_feedback:
                # Update existing feedback
                existing_feedback.rating = int(rating)
                existing_feedback.helped = helped_bool
                existing_feedback.pacing = pacing
                flash('Feedback updated successfully!', 'success')
            else:
                # Create new feedback
                practice_feedback = PracticeFeedback(
                    practice_id=practice.id,
                    user_id=current_user.id,
                    rating=int(rating),
                    helped=helped_bool,
                    pacing=pacing
                )
                db.session.add(practice_feedback)
                flash('Thank you for your feedback!', 'success')

            db.session.commit()
            return redirect(url_for('thank'))

        # Check if there's already feedback to display
        existing_feedback = PracticeFeedback.query.filter_by(practice_id=practice.id).first()

        return render_template('feedback.html',
                               practice=practice,
                               existing_feedback=existing_feedback)

    @app.route('/thank')
    @login_required
    def thank():
        # Get user's most recent check-in to determine time of day
        today = date.today()
        latest_checkin = CheckIn.query.filter(
            CheckIn.user_id == current_user.id,
            db.func.date(CheckIn.created_at) == today
        ).order_by(CheckIn.created_at.desc()).first()

        time_of_day = latest_checkin.time_of_day if latest_checkin else None

        return render_template('thank.html', time_of_day=time_of_day)

    @app.route('/')
    def index():
        return render_template('index.html')