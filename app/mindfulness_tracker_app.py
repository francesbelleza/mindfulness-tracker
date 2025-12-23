# By Frances Belleza
# Function: This file is like main()
#              it defines my routes & logic

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, date
from app.models import User, CheckIn
from app import db

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
        return render_template('practice.html')

    @app.route('/')
    def index():
        return render_template('index.html')