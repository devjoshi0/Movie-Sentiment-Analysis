import requests
from main import api_key


def get_movie_ids():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    response = requests.get(url)
    movie_list = response.json()["results"]
    return [movie["id"] for movie in movie_list]

def get_tv_ids():
    url = f"https://api.themoviedb.org/3/tv/popular?api_key={api_key}"
    response = requests.get(url)
    tv_list = response.json()["results"]
    return [tv["id"] for tv in tv_list]

def obtain_embeded_trailers(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"
    response = requests.get(url)
    video_list = response.json()["results"]
    return [video["key"] for video in video_list]

def get_movie_runtime(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json().get("runtime", "N/A")

def get_network_url(network_id):
    url = f"https://api.themoviedb.org/3/network/{network_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json().get("homepage", "#")

def get_new_releases():
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}"
    response = requests.get(url)
    movie_list = response.json()["results"]
    return [movie["id"] for movie in movie_list]

def get_trending():
    url = f"https://api.themoviedb.org/3/trending/all/day?api_key={api_key}"
    response = requests.get(url)
    movie_list = response.json()["results"]
    return [movie["id"] for movie in movie_list]

def get_popular_movies():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    response = requests.get(url)
    movie_list = response.json()["results"]
    return [movie["id"] for movie in movie_list]

def get_popular_tv():
    url = f"https://api.themoviedb.org/3/tv/popular?api_key={api_key}"
    response = requests.get(url)
    tv_list = response.json()["results"]
    return [tv["id"] for tv in tv_list]