from flask import Blueprint, request, jsonify
from .models import db, Url
import string
import secrets

main = Blueprint('main', __name__)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_unique_short_code():
    while True:
        candidate = generate_short_code();
        if not db.session.query(Url).filter_by(shortCode=candidate).first():
            return candidate
        
def get_url_item(short_code):
    return Url.query.filter(Url.shortCode==short_code).first_or_404()    


@main.route("/shorten", methods=["POST"])
def create_code():
    data = request.json
    if 'url' not in data:
        return (jsonify({
            "message": "you must provide a 'url' field"
        }, 400))
    
    short_code = generate_short_code()
    new_url = Url(url=data['url'], shortCode=short_code)
    db.session.add(new_url)
    db.session.commit()
    item = get_url_item(short_code)
    return jsonify(item.to_json()), 201

@main.route("/shorten/<short_code>", methods=["GET"])
def get_url(short_code):
    item = get_url_item(short_code)
    item.accessCount += 1
    db.session.commit()
    return jsonify(item.to_json()), 200

@main.route("/shorten/<short_code>", methods=["PUT"])
def update_url(short_code):
    item = get_url_item(short_code)
    data = request.json
    item.url = data.get('url', item.url)
    db.session.commit()
    item = get_url_item(short_code)
    return jsonify(item.to_json()), 200

@main.route("/shorten/<short_code>", methods=["DELETE"])
def delete_short_code(short_code):
    item = get_url_item(short_code)
    db.session.delete(item)
    db.session.commit()
    return '', 204

@main.route("/stats/<short_code>", methods=["GET"])
def get_stats(short_code):
    item = get_url_item(short_code)
    return jsonify(item.to_json() | {"access_count": item.accessCount}), 200
    


