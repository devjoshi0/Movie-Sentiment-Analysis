# localhost:8000/create_contact
from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([contact.to_json() for contact in contacts])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)