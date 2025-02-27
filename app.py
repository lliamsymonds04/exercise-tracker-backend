from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from extensions import db, bcrypt, login_manager
from blueprints.auth import auth
from blueprints.exercise_handler import exercise_handler


def create_app():
    new_app = Flask(__name__)
    CORS(new_app, supports_credentials=True, origins=["http://localhost:5173"])

    load_dotenv()

    #setup database
    new_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    new_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    new_app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
    # new_app.config['PERMANENT_SESSION_LIFETIME'] = 604800  # 7 days
    # new_app.config["REMEMBER_COOKIE_DURATION"] = 604800

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


app = create_app()


if __name__ == '__main__':
    app.run(debug=False)