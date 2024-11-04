# app/tmdb_client.py
import hashlib
import json

import requests
from flask import session


class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"
    _instance = None

    def __new__(cls, api_key=None):
        if not cls._instance:
            cls._instance = super(TMDBClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key):
        # Ensure __init__ runs only once by checking if api_key is already set
        if not hasattr(self, 'api_key'):
            self.api_key = api_key
            self.cache = {}  # Initialize an empty cache dictionary
            print("Created new TMDBClient instance")

    def _generate_cache_key(self, endpoint, params):
        """Generate a unique cache key based on the endpoint and parameters."""
        # Use a hash function to create a unique key for the request
        key_string = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def _make_request(self, endpoint, params=None):
        if params is None:
            params = {}
        else:
            params = params.copy()  # Make a copy to avoid modifying the original

        params['language'] = session.get('language', 'en-US')
        params['api_key'] = self.api_key

        # Generate a cache key for the request
        cache_key = self._generate_cache_key(endpoint, params)

        # Check if the response is already cached
        if cache_key in self.cache:
            print("Using cached response")
            return self.cache[cache_key]

        print("created new request")
        # Make the request if not cached
        response = requests.get(f"{self.BASE_URL}{endpoint}", params=params)
        response_data = response.json()

        # Store the response in cache
        self.cache[cache_key] = response_data

        return response_data

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

    def trending_all(self, page=1, time_window="day"):
        params = {"page": page}
        return self._make_request(f"/trending/all/{time_window}", params)

    def get_details(self, media_type, item_id):
        return self._make_request(f"/{media_type}/{item_id}")

    def upcoming_movies(self):
        return self._make_request("/movie/upcoming")

    def top_rated_movies(self):
        return self._make_request("/movie/top_rated")

    def top_rated_tv(self):
        return self._make_request("/tv/top_rated")

    def discover_animated(self, media_type, page=1):

        # Set up the parameters for the request
        params = {
            "page": page,
            "with_genres": 16,  # Genre ID for Animation
            "without_keywords": "155477|41172|256466|195669|198385",  # Keywords to filter results
        }

        # Make the request to the appropriate endpoint
        return self._make_request(f"/discover/{media_type}", params)

    def get_similar(self, item_id, page=1):
        params = {"page": page}
        return self._make_request(f"/movie/{item_id}/similar", params)
