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

@app.route("/watchlist/<int:movie_id>", methods=["POST"])
def add_to_watchlist(movie_id):
    user_ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    watchlist = Watchlist.query.filter_by(user_ip=user_ip, movie_id=movie_id).first()
    if watchlist:
        return redirect(url_for("index"))

    movie_exists = Movie.query.get(movie_id)
    if not movie_exists:
        movieid = get_movie_ids()
        tvid = get_tv_ids()

        try:
            if movie_id in movieid:
                movie_details = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}").json()
                movie = Movie(id=movie_id, title=movie_details["title"], description=movie_details["overview"], image=movie_details["poster_path"])
                db.session.add(movie)
                db.session.commit()
            elif movie_id in tvid:
                tv_details = requests.get(f"https://api.themoviedb.org/3/tv/{movie_id}?api_key={api_key}").json()
                tv = Movie(id=movie_id, title=tv_details["name"], description=tv_details["overview"], image=tv_details["poster_path"])
                db.session.add(tv)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding movie/TV show: {e}")

    new_watchlist_item = Watchlist(user_ip=user_ip, movie_id=movie_id)
    db.session.add(new_watchlist_item)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/watchlist/<int:movie_id>/delete", methods=["POST"])
def delete_from_watchlist(movie_id):
    user_ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    Watchlist.query.filter_by(user_ip=user_ip, movie_id=movie_id).delete()
    db.session.commit()
    return redirect(url_for("watchlist"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)