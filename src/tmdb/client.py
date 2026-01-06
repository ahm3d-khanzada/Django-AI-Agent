# tmdb/client.py  (or wherever your TMDB functions live)

import requests
from django.conf import settings

def get_header():
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_API_KEY}"
    }

def search_movie(query: str, page: int = 1, raw: bool = False):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "query": query,
        "page": page,
        "include_adult": False,
        "language": "en-US"
    }
    headers = get_header()
    response = requests.get(url=url, headers=headers, params=params)  # Fixed: param → params

    if raw:
        return response
    return response.json()

def movies_details(movie_id: int, raw: bool = False):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "include_adult": False,
        "language": "en-US"
    }
    headers = get_header()
    response = requests.get(url=url, headers=headers, params=params)

    if raw:
        return response
    return response.json()