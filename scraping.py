'''
this script, scrapes reviews from IMDB and potentially other review sites such as Rotten Tomatoes
to be processed for the sentiment analysis model.

'''

import string
import requests
from bs4 import BeautifulSoup
import pandas
import json
import os
from dotenv import load_dotenv
from sentiment import analyze_sentiment, preprocess_text

load_dotenv("env/.env")
api_key = os.getenv('API_KEY')


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
    return reviews

def store_reviews(reviews):
    analyzed_reviews = []
    for review in reviews:
        sentiment_score = analyze_sentiment(review)
        analyzed_reviews.append({"review" : review, "sentiment_score" : sentiment_score * 100})
        for i in range(len(reviews)):
            print(reviews[i])
    return analyzed_reviews

def convert_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    movie_name = input("Enter the name of the movie: ")
    
    imdb_id =extract_id(movie_name, api_key)
    if imdb_id.startswith('tt'):
        print(f"The IMDb ID for '{movie_name}' is: {imdb_id}")
        print(f"https://www.imdb.com/title/{imdb_id}/reviews/?ref_=tt_ov_rt")
        reviews = scrape_imdb_reviews(imdb_id)
        cleaned_reviews = store_reviews(reviews)
        convert_to_json(cleaned_reviews, f"reviews/{movie_name}.json")
    else:
        print(imdb_id)

if __name__ == "__main__":
    main()