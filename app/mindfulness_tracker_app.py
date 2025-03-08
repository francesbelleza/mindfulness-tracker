# Created by Frances Belleza -  Mindfulness Tracker
#
# File: app/ mindfulness_tracker_app.py
# Function: This file is like main()
#              it defines my routes & logic

from app import app
@app.route('/mindfulness-tracker-home')
def home():
    return "Hello & welcome to mindfulness app tracker"