from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure the database — change this if you're using something else
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///boxing.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # optional, but recommended

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
