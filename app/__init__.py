# app/__init__.py
import logging
import os
from logging.handlers import RotatingFileHandler

import sqlalchemy
from flask import Flask,current_app
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

Base = sqlalchemy.orm.declarative_base()

def create_app():
    app = Flask(__name__)
    # Load configuration from config file
    app.config.from_object(Config)

    # Set up logging after loading the app config
    setup_logging(app)

    # Initialize app with extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as routes_bp
    app.register_blueprint(routes_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Create a rotating file handler
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))

    # Set the logging level
    file_handler.setLevel('INFO')

    # Add the file handler to the app logger
    app.logger.addHandler(file_handler)

    # Optionally set the logging level for the app
    app.logger.setLevel('INFO')
