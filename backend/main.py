# localhost:8000/create_contact
import requests
from flask import Flask, render_template, redirect, url_for, request
from config import Config
from flask_cors import CORS
from models import db, Movie, Watchlist
from utils import get_movie_ids, get_tv_ids, embeded_youtube, get_movie_runtime, get_trending, get_popular_movies, get_popular_tv, get_new_releases

app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app, origins="*")
db.init_app(app)
app.app_context().push()

#home page
@app.route("/home")
def home():
    trending = get_trending()
    popular_movies = get_popular_movies()
    popular_tv = get_popular_tv()
    new_releases = get_new_releases()
    return render_template("index.html", trending=trending, popular_movies=popular_movies, popular_tv=popular_tv, new_releases=new_releases)

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

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        search = request.form['movie_name']
        url = f'https://api.themoviedb.org/3/search/multi?api_key={api_key}&query={search}'
        response = requests.get(url)
        r = response.json()
        result = r['results']
        for i in result:
            if i['media_type'] == 'movie':
                i['media_type'] = 'Movie'
            elif i['media_type'] == 'tv':
                i['media_type'] = 'TV Show'
        return render_template('search_results.html', result=result)
    

@app.route('/details/<movie_id>')
def details(movie_id):
    movieid = get_movie_ids()
    tv_id = get_tv_ids()
    try:
        if int(movie_id) in movieid:
            url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
            response = requests.get(url)
            data = response.json()
            name = data['title']
            poster = f'https://image.tmdb.org/t/p/w500{data["poster_path"]}'
            year = data['release_date'].split('-')[0]
            overview = data['overview']
            rating = data['vote_average']
            vote_count = data['vote_count']
            trailer = embeded_youtube(movie_id) if 'videos' in data else None
            category = data['genres']
            category_name = [i['name'] for i in category]
            runtime = get_movie_runtime(movie_id)
            return render_template('details.html', name=name, poster=poster, year=year, overview=overview, rating=rating, vote_count=vote_count, category_name=category_name, trailer=trailer, runtime=runtime)
        elif int(movie_id) in tv_id:
            url = f'https://api.themoviedb.org/3/tv/{movie_id}?api_key={api_key}'
            response = requests.get(url)
            data = response.json()
            name = data['name']
            poster = f'https://image.tmdb.org/t/p/w500{data["poster_path"]}'
            overview = data['overview']
            rating = data['vote_average']
            vote_count = data['vote_count']
            trailer = embeded_youtube(movie_id) if 'videos' in data else None
            category = data['genres']
            category_name = [i['name'] for i in category]
            return render_template('details.html', name=name, poster=poster, overview=overview, rating=rating, vote_count=vote_count, category_name=category_name, trailer=trailer)
    except Exception as e:
        print(e)
        return render_template('index.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=8080)
