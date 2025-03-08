# Created by Frances Belleza -  Mindfulness Tracker
#
# File: app/ __init__.py
# Function: This file creates a flask app

from flask import Flask #renders template

app = Flask(__name__) #creates flask app

#imports my routes
from app import mindfulness_tracker_app
