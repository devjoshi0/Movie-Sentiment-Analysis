#contains database models (2)
#what fields we need how we will add them how we will delete them
from config import db
from flask_sqlalchemy import SQLAlchemy

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    watchlist = db.relationship('Watchlist', backref='movie', lazy=True)



class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)