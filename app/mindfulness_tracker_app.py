# Created by Frances Belleza -  Mindfulness Tracker
#
# File: app/ mindfulness_tracker_app.py
# Function: This file is like main()
#              it defines my routes & logic

from app import app
from flask import render_template

@app.route('/')
@app.route('/mindfulness-tracker-home')
def home():
    user_logged_in = False #need to change to True to test dashboard button
    return render_template('index.html', user_logged_in=user_logged_in)