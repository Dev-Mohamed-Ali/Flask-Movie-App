from flask import Blueprint

# Create a blueprint instance for main routes
bp = Blueprint('main', __name__)

# Import routes to register them with the blueprint
from app.main import routes
