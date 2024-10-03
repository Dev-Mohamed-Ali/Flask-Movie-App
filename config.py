# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///MovieApp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    MAIL_SERVER = 'smtp.example.com'  # Replace with your SMTP server
    MAIL_PORT = 587  # For TLS
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # Your email username
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # Your email password
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USER')  # Default sender email
