'''
this script, scrapes reviews from IMDB and potentially other review sites such as Rotten Tomatoes
to be processed for the sentiment analysis model.

'''

import string
import requests
from bs4 import BeautifulSoup
import pandas


user_input = input("Enter the movie name: ")

imdb_user_reviews_url = "https://www.imdb.com/title/tt4154796/"
imdb_critic_reviews_url = ""