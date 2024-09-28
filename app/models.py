# app/models.py
from app import db, login_manager, Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model,Base):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    recommendations = db.relationship('Recommendation', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer)
    item_type = db.Column(db.String(10))  # 'movie' or 'series'
    title = db.Column(db.String())
    overview = db.Column(db.String())
    poster_path = db.Column(db.String())
    rating = db.Column(db.Float)