'''
this script, scrapes reviews from IMDB and potentially other review sites such as Rotten Tomatoes
to be processed for the sentiment analysis model.

'''

import string
import requests
from bs4 import BeautifulSoup
import pandas
import json


user_input = "avatar"



# Function to scrape IMDB reviews
def scrape_imdb_reviews(movie_name):
    
    search_url = f"https://www.imdb.com/find?q={movie_name}&s=tt&ttype=ft&ref_=fn_ft"
    search_response = requests.get(search_url)
    search_soup = BeautifulSoup(search_response.text, 'html.parser')
    result_text = search_soup.find('td', class_='result_text')
    if result_text is not None:
        movie_id = result_text.find('a')['href'].split('/')[2]
        print(movie_id)
    else:
        movie_id = None  # or handle the case when movie_id is not found


    reviews_url = f"https://www.imdb.com/title/tt0499549/reviews/?ref_=tt_ov_rt"
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


scrape_imdb_reviews(user_input)