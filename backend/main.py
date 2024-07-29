# localhost:8000/create_contact
from flask import Flask, render_template, redirect, url_for, request
from config import Config
from models import db, Movie, Watchlist

api_key = "06c3064b912363d278bee2a70f9bdc2b"

@app.route("/home")
def home():
    trending = ()
    return jsonify([contact.to_json() for contact in contacts])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)