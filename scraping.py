'''
this script, scrapes reviews from IMDB and potentially other review sites such as Rotten Tomatoes
to be processed for the sentiment analysis model.

'''

import string
import requests
from bs4 import BeautifulSoup
import pandas
import json
from sentiment import *

user_input = "avatar"

def extract_id(movie_name, api_key):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            imdb_id = data.get('imdbID')
            return imdb_id
        else:
            return "Movie not found!"
    else:
        return "Error occured"


def scrape_imdb_reviews(movie_id):

    reviews_url = f"https://www.imdb.com/title/{movie_id}/reviews/?ref_=tt_ov_rt"
    reviews_response = requests.get(reviews_url)
    reviews_soup = BeautifulSoup(reviews_response.text, 'html.parser')
    review_containers = reviews_soup.find_all('div', class_='review-container')

    reviews = []
    for container in review_containers:
        review = container.find('div', class_='text show-more__control').text.strip()
        reviews.append(review)

    json_data = json.dumps(reviews[:100])
    with open('reviews.json', 'w') as file:
        file.write(json_data)


def main():
    movie_name = input("Enter the name of the movie: ")
    api_key = '6112d89c'
    
    imdb_id =extract_id(movie_name, api_key)
    if imdb_id.startswith('tt'):
        print(f"The IMDb ID for '{movie_name}' is: {imdb_id}")
        print(f"https://www.imdb.com/title/{imdb_id}/reviews/?ref_=tt_ov_rt")
        scrape_imdb_reviews(imdb_id)
    else:
        print(imdb_id)

if __name__ == "__main__":
    main()