import requests
from main import api_key


def get_movie_ids():
    url = f"https://api.themoviedb.org/3/trending/movie/popular?api_key={api_key}"
    response = requests.get(url)
    movie_list = response.json()["results"]
    return [movie["id"] for movie in movie_list]

def get_tv_ids():
    url = f"https://api.themoviedb.org/3/trending/tv/popular?api_key={api_key}"
    response = requests.get(url)
    tv_list = response.json()["results"]
    return [tv["id"] for tv in tv_list]