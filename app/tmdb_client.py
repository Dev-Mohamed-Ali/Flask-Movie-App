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
        return self._make_request("/search/multi", {"query": query, "page": page})

    def discover(self, media_type, page=1):
        return self._make_request(f"/discover/{media_type}", {"page": page})

    def trending(self, time_window="week"):
        return self._make_request(f"/trending/all/{time_window}")

    def trending_with_type(self,media_type,page, time_window="week"):
        return self._make_request(f"/trending/{media_type}/{time_window}",{"page": page})

    def get_details(self, media_type, item_id):
        return self._make_request(f"/{media_type}/{item_id}")