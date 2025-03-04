from flask import Flask
from flask_cors import CORS
import os

from extensions import db, bcrypt, login_manager, DATABASE_URL, SECRET_KEY
from blueprints.auth import auth
from blueprints.exercise_handler import exercise_handler


def create_app():
    new_app = Flask(__name__)
    CORS(new_app, supports_credentials=True, origins=["http://localhost:*", "https://lliams-exercise-tracker.vercel.app"])


    #setup database
    new_app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    new_app.config['SECRET_KEY'] = SECRET_KEY
    new_app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    db.init_app(new_app)
    bcrypt.init_app(new_app)
    login_manager.init_app(new_app)

    #blueprints
    new_app.register_blueprint(auth)
    new_app.register_blueprint(exercise_handler, url_prefix='/exercise')

    # Initialize the database
    with new_app.app_context():
        db.create_all()

    return new_app




if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)