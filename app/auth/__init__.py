from flask import Blueprint

# Create a blueprint instance for auth
bp = Blueprint('auth', __name__)

# Import routes to register them with the blueprint
from app.auth import routes
