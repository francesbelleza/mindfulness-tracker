# By Frances Belleza
# initialize to be a lib

import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # imports my routes
    with app.app_context():
        from app import mindfulness_tracker_app
        mindfulness_tracker_app.initial_routes(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

login_manager.login_view = 'login'
login_manager.login_message = None   # suppress the default flash
login_manager.unauthorized_handler(lambda: (render_template('login_required.html'), 401))

