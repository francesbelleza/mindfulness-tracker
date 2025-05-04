# By Frances Belleza
# Function: This file is like main()
#              it defines my routes & logic

from flask import render_template
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import db
#from app.models import TestModel

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

    # ensure your other routes are protected as needed
    @app.route('/check-in')
    @login_required
    def check_in():
        return render_template('check_in.html')

    @app.route('/')
    def index():
        return render_template('index.html')