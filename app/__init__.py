from flask import Flask
from .models import db
from .routes import main
import os


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URI')
    app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(main)
    return app