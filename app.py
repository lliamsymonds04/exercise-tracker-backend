from flask import Flask
from dotenv import load_dotenv
import os

from extensions import db, bcrypt, login_manager
from blueprints.login import auth


def create_app():
    new_app = Flask(__name__)

    #setup database
    load_dotenv()

    database_url = os.getenv('DATABASE_URL')
    new_app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    new_app.config['PERMANENT_SESSION_LIFETIME'] = 604800  # 7 days

    db.init_app(new_app)
    bcrypt.init_app(new_app)
    login_manager.init_app(new_app)

    #blueprints
    new_app.register_blueprint(auth)

    # Initialize the database
    with new_app.app_context():
        db.create_all()

    return new_app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)