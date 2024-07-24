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




# Scrape reviews from IMDB
reviews_url = f"https://www.imdb.com/title/tt0499549/reviews/?ref_=tt_ov_rt"
reviews_response = requests.get(reviews_url)
reviews_soup = BeautifulSoup(reviews_response.text, 'html.parser')
review_containers = reviews_soup.find_all('div', class_='review-container')

# Store reviews in a list
reviews = []
for container in review_containers:
    review = container.find('div', class_='text show-more__control').text.strip()
    reviews.append(review)

# Save reviews to a JSON file
json_data = json.dumps(reviews[:100])
with open('reviews.json', 'w') as file:
    file.write(json_data)

