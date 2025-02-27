from datetime import datetime

from flask import request, jsonify, Blueprint, session
from flask_login import login_required, current_user
from sqlalchemy import distinct

from models import db, Exercise, Set

exercise_handler = Blueprint('exercise_handler', __name__)

@exercise_handler.route('/track', methods=['POST'])
@login_required
def track():
    data = request.get_json()

    if not data or 'exercise_name' in data:
        return jsonify({"error": "exercise_name is required"}), 400

    exercise_name = data.get('exercise_name')


    new_exercise = Exercise(exercise_name=exercise_name, user_id=current_user.id, date=datetime.now())
    db.session.add(new_exercise)
    db.session.commit()

    return jsonify({"exercise_id": new_exercise.id})


@exercise_handler.route('/add_set', methods=['POST'])
@login_required
def add_sets():
    data = request.get_json()


@exercise_handler.route('/get_names', methods=['GET'])
@login_required
def get_names():
    names = db.session.query(distinct(Exercise.exercise_name)).filter_by(user_id=current_user.id).all()

    return jsonify([name[0] for name in names])


@exercise_handler.route('/log', methods=['POST'])
@login_required
def log():
    data = request.get_json()

    if not data or "exercise_name" not in data or "sets" not in data:
        return jsonify({"error": "exercise name and sets are required"}), 400

    exercise_name: str = data.get('exercise_name')
    sets: list[dict[str, int]] = data.get('sets')
    note: str = data.get('note')

    if not exercise_name or not sets:
        return jsonify({"error": "exercise_name and sets are required"}), 400

    if type(sets) is not list:
        return jsonify({"error": "sets must be a list"}), 401

    if len(sets) > 10 or len(sets) < 1:
        return jsonify({"error": "Sets size is to big"}), 401

    new_exercise = Exercise(exercise_name=exercise_name, user_id=current_user.id, date=datetime.now())

    set_objs = []
    for i in range(len(sets)):
        set_data = sets[i]

        if "weight" not in set_data or "reps" not in set_data:
            return jsonify({"error": "weight or reps is required"}), 402

        new_set = Set(exercise_id=new_exercise.id, weight=set_data["weight"], reps=set_data["reps"], set_number=(i+1))
        set_objs.append(new_set)

    db.session.add(new_exercise)
    for set_obj in set_objs:
        db.session.add(set_obj)

    db.session.commit()

    return jsonify({"success": True})
