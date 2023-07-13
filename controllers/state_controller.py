from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.state import State, state_schema, states_schema
from init import db

state_bp = Blueprint('state_bp', __name__)


@state_bp.route('/states', methods=['GET'])
@jwt_required()
def get_all_states():
    all_states = State.query.all()
    result = states_schema.dump(all_states)
    return jsonify(result)


@state_bp.route('/state', methods=['POST'])
@jwt_required()
def add_state():
    state_name = request.json['state_name']
    new_state = State(state_name=state_name)

    db.session.add(new_state)
    db.session.commit()

    return state_schema.jsonify(new_state), 201


@state_bp.route('/state/<id>', methods=['DELETE'])
@jwt_required()
def delete_state(id):
    current_user = current_identity
    if current_user.is_admin:
        state = State.query.get(id)
        if state is None:
            return jsonify({'error': 'State not found'}), 404

        db.session.delete(state)
        db.session.commit()

        return state_schema.jsonify(state)
    else:
        return jsonify({'error': 'Permission denied'}), 403
