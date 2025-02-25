from datetime import datetime

from flask import request, jsonify, Blueprint, session
from flask_login import login_required, current_user
from sqlalchemy import distinct

from models import db, Exercises

exercise_handler = Blueprint('exercise_handler', __name__)

@exercise_handler.route('/track', methods=['POST'])
@login_required
def track():
    data = request.get_json()
    exercise_name = data.get('exercise_name')

    new_exercise = Exercises(exercise_name=exercise_name, user_id=current_user.id, date=datetime.now())
    db.session.add(new_exercise)
    db.session.commit()

    return jsonify({"exercise_id": new_exercise.id})



# @exercise_handler.route('/add_set', methods=['POST'])
# @login_required
# def add_set():
#


@exercise_handler.route('/get_names', methods=['GET'])
@login_required
def get_names():
    names = db.session.query(distinct(Exercises.exercise_name)).filter_by(user_id=current_user.id).all()

    return jsonify([name[0] for name in names])