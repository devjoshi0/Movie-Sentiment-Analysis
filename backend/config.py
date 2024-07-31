#building api (1)
#basic configuration this happens first
#data
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///watchlist.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
