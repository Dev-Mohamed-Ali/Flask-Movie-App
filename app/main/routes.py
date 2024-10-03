from flask import render_template, request, current_app
from flask_login import login_required, current_user
from app.main import bp
from app.tmdb_client import TMDBClient
import app.api.routes as api


@bp.route('/')
def index():
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    trending_feed = tmdb_client.trending()
    return render_template('main/index.html', trending=trending_feed['results'])

@bp.route('/search')
def search():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    results = tmdb_client.search(query, page)
    print(results)
    return render_template('main/search.html', results=results['results'], query=query, page=page)

@bp.route('/discover/<media_type>')
def discover(media_type):
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    results = tmdb_client.discover(media_type, page)
    return render_template('main/discover.html', results=results['results'], media_type=media_type, page=page)

@bp.route('/details/<media_type>/<int:item_id>')
def details(media_type, item_id):
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    item_details = tmdb_client.get_details(media_type, item_id)
    return render_template('main/details.html', item=item_details, media_type=media_type)

@bp.route('/trending/<media_type>')
def trending(media_type):
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    results = tmdb_client.trending_with_type(media_type,page)
    return render_template('main/trending.html', results=results['results'], media_type=media_type, page=page)


@bp.route('/recommendations')
@login_required
def show_user_recommendations():
    try:
        user_id = current_user.id
        recommendations = api.fetch_recommendations(user_id)  # Use the same function to fetch recommendations

        if not recommendations:
            recommendations = []  # Treat it as no recommendations if None is returned
    except Exception as e:
        recommendations = []
        current_app.logger.error(f"Error occurred while fetching recommendations for user {current_user.id}: {str(e)}")

    return render_template('main/user_recommendations.html', user_recommendations=recommendations)