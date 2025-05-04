# By Frances Belleza
# initialize to be a lib

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # imports my routes
    with app.app_context():
        from app import mindfulness_tracker_app
        mindfulness_tracker_app.initial_routes(app)

    return app
