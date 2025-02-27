from flask import request, jsonify, Blueprint, session
from flask_login import login_user, login_required, logout_user, current_user
from app import bcrypt

from models import db, Users
from extensions import login_manager

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

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

    return jsonify({"message": "Account created successfully!"}), 201


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
        return jsonify({"message": "Logged in successfully!", "user": {"username": user.username}})

    return jsonify({"error": "Login failed. Check your credentials."}), 401

@auth.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return jsonify({"message": f"Hello, {current_user.username}! Welcome to your dashboard."})

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"})