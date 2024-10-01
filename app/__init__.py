# app/__init__.py
import sqlalchemy
from flask import Flask
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

    # Initialize app with extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app