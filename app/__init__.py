# By Frances Belleza
# initialize to be a lib

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # imports my routes
    with app.app_context():
        from app import mindfulness_tracker_app
        mindfulness_tracker_app.initial_routes(app)

    return app
