from flask import Blueprint

# Create a blueprint instance for the API
bp = Blueprint('api', __name__)

# Import routes to register them with the blueprint
from app.api import routes
