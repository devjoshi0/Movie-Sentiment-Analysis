# localhost:8000/create_contact
from flask import Flask, render_template, redirect, url_for, request
from config import Config
from models import db, Movie, Watchlist
from utils import *

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.app_context().push()

#home page
@app.route("/home")
def home():
    trending = get_trending()
    popular_movies = get_popular_movies()
    popular_tv = get_popular_tv()
    new_releases = get_new_releases()
    return render_template("home.html", trending=trending, popular_movies=popular_movies, popular_tv=popular_tv, new_releases=new_releases)

@app.route("/watchlist")
def watchlist():
    user_id = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    watchlist = Watchlist.query.filter_by(user_id=user_id).all()
    movies = [Movie.query.get(watch.movie_id) for watch in watchlist]
    return render_template("watchlist.html", movies=movies)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)