from flask import request, jsonify, Blueprint, session, make_response
from flask_login import login_user, login_required, logout_user, current_user
import jwt
import datetime

# from app import bcrypt
from extensions import login_manager, bcrypt, SECRET_KEY
from models import db, Users

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

def make_login_token(username: str):
    token = jwt.encode(
        {"user": username, "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)},
        key=SECRET_KEY,
        algorithm="HS256",
    )

    return token

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Expecting JSON from the React app
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username: str = data.get('username').strip()
    password: str = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password cannot be empty"}), 400

    #check if username exists
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already taken"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = Users(username=username, passwordHash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    response = make_response({"message": "Account created successfully!"})
    response.set_cookie('token', make_login_token(username), httponly=True, samesite='Strict')
    return response
    # return jsonify({"message": "Account created successfully!"}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400

    password = data.get('password')
    username = data.get('username')
    user = Users.query.filter_by(username=username).first()


    if user and bcrypt.check_password_hash(user.passwordHash, password):
        login_user(user)
        session.permanent = True
        # return jsonify({"message": "Logged in successfully!", "user": {"username": user.username}})
        response = make_response({"message": "Logged in successfully!", "user": {"username": user.username}})
        response.set_cookie('token', make_login_token(username), httponly=True, samesite='Strict')
        return response

    return jsonify({"error": "Login failed. Check your credentials."}), 401

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    # return jsonify({"message": "Logged out successfully!"})
    response = make_response(jsonify({"message": "Logged out"}))
    response.set_cookie("token", "", expires=0)  # Remove the token
    return response

@auth.route("/me", methods=["GET"])
def get_current_user():
    return jsonify({"user": current_user.id})