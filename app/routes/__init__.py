from flask import Blueprint, render_template, request, current_app
from app.tmdb_client import TMDBClient

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    trending_feed = tmdb_client.trending()
    return render_template('index.html', trending=trending_feed['results'])

@bp.route('/search')
def search():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    results = tmdb_client.search(query, page)
    print(results)
    return render_template('search.html', results=results['results'], query=query, page=page)

@bp.route('/discover/<media_type>')
def discover(media_type):
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    results = tmdb_client.discover(media_type, page)
    return render_template('discover.html', results=results['results'], media_type=media_type, page=page)

@bp.route('/details/<media_type>/<int:item_id>')
def details(media_type, item_id):
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    item_details = tmdb_client.get_details(media_type, item_id)
    return render_template('details.html', item=item_details,media_type=media_type)

@bp.route('/trending/<media_type>')
def trending(media_type):
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    results = tmdb_client.trending_with_type(media_type,page)
    return render_template('trending.html', results=results['results'], media_type=media_type, page=page)
