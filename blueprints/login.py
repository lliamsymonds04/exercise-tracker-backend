from flask import request, jsonify, Blueprint, session
from flask_login import login_user, login_required, logout_user, current_user
from app import bcrypt

from models import db, User

auth = Blueprint('login', __name__)

@auth.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()  # Expecting JSON from the React app
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Account created successfully!"}), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        session.permanent = True  # To enable session permanence
        return jsonify({"message": "Logged in successfully!", "user": {"username": user.username, "email": user.email}})
    else:
        return jsonify({"message": "Login failed. Check your credentials."}), 401

@auth.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return jsonify({"message": f"Hello, {current_user.username}! Welcome to your dashboard."})

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"})