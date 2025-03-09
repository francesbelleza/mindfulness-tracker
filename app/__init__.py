# Created by Frances Belleza -  Mindfulness Tracker
#
# File: app/ __init__.py
# Function: This file creates a flask app

import os
from flask import Flask #renders template

app = Flask(__name__, static_folder="../static") #creates flask app

#imports my routes
from app import mindfulness_tracker_app
