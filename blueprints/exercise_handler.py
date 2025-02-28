from datetime import datetime

from flask import request, jsonify, Blueprint, session
from flask_login import login_required, current_user
from sqlalchemy import distinct

from models import db, Exercise, Set
from util.binary_insert import binary_insertion

exercise_handler = Blueprint('exercise_handler', __name__)

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

    if len(sets) > 5 or len(sets) < 1:
        return jsonify({"error": "Sets size is to big"}), 401

    new_exercise = Exercise(exercise_name=exercise_name, user_id=current_user.id, note=note)

    db.session.add(new_exercise)
    db.session.flush()  # Flush to assign an ID to new_exercise

    set_objs = []
    for i, set_data in enumerate(sets):
        if "weight" not in set_data or "reps" not in set_data:
            return jsonify({"error": "weight and reps are required"}), 402

        new_set = Set(exercise_id=new_exercise.id, weight=set_data["weight"], reps=set_data["reps"], set_number=i + 1)
        set_objs.append(new_set)

    db.session.add_all(set_objs)
    db.session.commit()

    return jsonify({"success": True})


@exercise_handler.route('/get_data', methods=['GET'])
@login_required
def get_data():
    exercise_name = request.args.get('exercise_name')
    before = request.args.get('before', datetime.now())  # Default to now
    amount = request.args.get('amount', 10, type=int)  # Convert to int

    if not exercise_name:
        return jsonify({"error": "exercise_name is required"}), 400

    # Get the exercises filtered by user and time
    exercises = (db.session.query(Exercise)
                 .filter_by(user_id=current_user.id)
                 .filter(Exercise.created_at < before)
                 .order_by(Exercise.created_at)
                 .limit(amount)
                 .all())

    # Extract exercise IDs
    exercise_ids = [e.id for e in exercises]

    # Get the sets related to these exercises
    sets = db.session.query(Set).filter(Set.exercise_id.in_(exercise_ids)).all()


    #now group them by ids and set number
    result = []
    for exercise in exercises:
        v = {
            "created_at": exercise.created_at,
            "note": exercise.note or "",
            "sets": [],
            "id": exercise.id,
        }
        binary_insertion(result, v, "created_at")

    print(result)

    id_mapping = {}
    for i in range(len(result)):
        v = result[i]
        id_mapping[v.get("id")] = i

    for s in sets:
        v = {
            "weight": s.weight,
            "reps": s.reps,
            "number": s.set_number
        }

        exercise = result[id_mapping[s.exercise_id]]
        binary_insertion(exercise.get("sets"), v, "number")


    #return the result
    return jsonify(result)