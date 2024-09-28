from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Recommendation
from app import db

bp = Blueprint('api', __name__)

@bp.route('/recommend', methods=['POST'])
@login_required
def add_recommendation():
    data = request.json

    item_id = data.get('item_id')
    item_type = data.get('item_type')
    title = data.get('title')
    overview = data.get('overview')
    poster_path = data.get('poster_path')
    rating = data.get('rating')

    recommendation = Recommendation(user_id=current_user.id, item_id=item_id, item_type=item_type,title=title,overview=overview,poster_path=poster_path, rating=rating)
    db.session.add(recommendation)
    db.session.commit()

    return jsonify({"message": "Recommendation added successfully"}), 201

@bp.route('/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    recommendations = Recommendation.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        "item_id": r.item_id,
        "item_type": r.item_type,
        "title": r.title,
        "overview": r.overview,
        "poster_path": r.poster_path,
        "rating": r.rating
    } for r in recommendations])