from flask import jsonify, request
from flask_login import login_required, current_user

from app import db
from app.api import bp
from app.models import Recommendation


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

# Reusable function to fetch recommendations for a user
def fetch_recommendations(user_id):
    recommendations = Recommendation.query.filter_by(user_id=user_id).all()
    if recommendations:
        return [{
            "item_id": r.item_id,
            "item_type": r.item_type,
            "title": r.title,
            "overview": r.overview,
            "poster_path": r.poster_path,
            "rating": r.rating
        } for r in recommendations]
    else:
        return None

@bp.route('/recommendations/<int:user_id>', methods=['GET'])
@login_required
def get_recommendations(user_id):
    recommendations = fetch_recommendations(user_id)
    if recommendations:
        return jsonify(recommendations), 200
    else:
        return jsonify({"message": "No recommendations"}), 200