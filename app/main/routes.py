from flask import render_template, request, current_app
from flask_login import login_required, current_user
from app.main import bp
from app.tmdb_client import TMDBClient
import app.api.routes as api


@bp.route('/')
def index():
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    upcoming_movies = tmdb_client.upcoming_movies()
    top_rated_movies = tmdb_client.top_rated_movies()
    top_rated_tv = tmdb_client.top_rated_tv()
    print(top_rated_tv)
    return render_template('main/index.html',
                           top_rated_movies=top_rated_movies['results'],
                           upcoming_movies=upcoming_movies['results'],
                           top_rated_tv=top_rated_tv['results'])


@bp.route('/search')
def search():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    results = tmdb_client.search(query, page)
    total_pages = results['total_pages']
    total_results = results['total_results']
    print(results)
    return render_template('main/search.html', results=results['results'], query=query, page=page,total_pages=total_pages, total_results=total_results)


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
    return render_template('main/item-details.html', item=item_details, media_type=media_type)



@bp.route('/trending/<media_type>')
def trending(media_type):
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    results = tmdb_client.trending_with_type(media_type, page)
    return render_template('main/trending.html', results=results['results'], media_type=media_type, page=page)


@bp.route('/trending')
def trending_all():
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])
    results = tmdb_client.trending_all(language='en-US', page=page)
    print(results)
    return render_template('main/trending.html', results=results['results'], page=page)


@bp.route('/animation/<media_type>')
def trending_animations_by_type(media_type):
    print(f"Requested media type: {media_type}")  # Log the media type
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])

    # Validate media type
    if media_type not in ['movie', 'tv']:
        return "Invalid media type. Please specify 'movie' or 'tv'.", 400

    # Fetch animated content based on media type
    results = tmdb_client.discover_animated(media_type, page)

    return render_template('main/animation.html',media_type=media_type, results=results['results'], page=page)


@bp.route('/animation')
def trending_animations():
    page = request.args.get('page', 1, type=int)
    tmdb_client = TMDBClient(current_app.config['TMDB_API_KEY'])

    # Fetch animated movies
    results_movies = tmdb_client.discover_animated('movie', page)
    # Fetch animated TV shows
    results_tv = tmdb_client.discover_animated('tv', page)

    # Combine results from both movies and TV shows
    combined_results = results_movies['results'] + results_tv['results']

    return render_template('main/animation.html', results=combined_results, page=page)


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
