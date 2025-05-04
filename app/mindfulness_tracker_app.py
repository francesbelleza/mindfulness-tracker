# By Frances Belleza
# Function: This file is like main()
#              it defines my routes & logic

from flask import render_template
from app.models import TestModel

def initial_routes(app):
    @app.route('/mindfulness-tracker-home')
    def home():
        user_logged_in = False #need to change to True to test dashboard button
        return render_template('index.html', user_logged_in=user_logged_in)