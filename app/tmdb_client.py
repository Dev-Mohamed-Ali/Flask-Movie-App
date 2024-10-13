# app/tmdb_client.py
import requests

class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(self, endpoint, params=None):
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        response = requests.get(f"{self.BASE_URL}{endpoint}", params=params)
        return response.json()

    def search(self, query, page=1):
        params = {
            "query": query,
            "page": page,
        }

        # Make the request
        response = self._make_request("/search/multi", params)

        person_count = 0
        video_count = 0
        filtered_results = []

        for result in response['results']:
            if result['media_type'] == 'person':
                person_count += 1
            elif result.get('video', False):
                video_count += 1
            else:
                filtered_results.append(result)

        # Update the 'total_results'
        response['results'] = filtered_results
        response['total_results'] -= (person_count + video_count)

        return response

    def discover(self, media_type, page=1):
        params = {"page": page}
        return self._make_request(f"/discover/{media_type}", params)

    def trending_with_type(self, media_type, page=1, time_window="week"):
        params = {"page": page}
        return self._make_request(f"/trending/{media_type}/{time_window}", params)

    def trending_all(self, language="en-US", page=1, time_window="day"):
        params = {"language": language, "page": page}
        return self._make_request(f"/trending/all/{time_window}", params)

    def get_details(self, media_type, item_id):
        return self._make_request(f"/{media_type}/{item_id}")

    def upcoming_movies(self, language="en-US"):
        params = {"language": language}
        return self._make_request("/movie/upcoming", params)

    def top_rated_movies(self, language="en-US"):
        params = {"language": language}
        return self._make_request("/movie/top_rated", params)

    def top_rated_tv(self, language="en-US"):
        params = {"language": language}
        return self._make_request("/tv/top_rated", params)

    def discover_animated(self, media_type, page=1, language="en-US"):

        # Set up the parameters for the request
        params = {
            "language": language,
            "page": page,
            "with_genres": 16,  # Genre ID for Animation
            "without_keywords": "155477|41172|256466|195669|198385",  # Keywords to filter results
        }

        # Make the request to the appropriate endpoint
        return self._make_request(f"/discover/{media_type}", params)