from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.state import State, state_schema, states_schema
from init import db

state_bp = Blueprint('state_bp', __name__, url_prefix='/state')


@state_bp.route('/<int:id>')
def get_all_states(id):
    stmt = db.select(State)
    state = db.session.scalars(stmt)

    return state_schema.dump(state)


@state_bp.route('/int:id>')
def get_city(id):
    stmt = db.select(State).filter_byt(id=id)
    state = db.session.scalar(stmt)
    if state:
        return state_schema.dump(state)
    else:
        return {'error': f'State not found with id {id}'}, 404


@state_bp.route('/state', methods=['POST'])
@jwt_required()
def add_state():
    body_data = request.get_json()

    state = State(
        state_name=body_data.get('state_name')
    )

    db.session.add(state)
    db.session.commit()

    return state_schema.dump(state), 201


@state_bp.route('/state/<id>', methods=['DELETE'])
@jwt_required()
def delete_state(id):
    stmt = db.select(State).filter_by(id=id)
    state = db.session.scalar(stmt)
    if state:
        db.session.delete(state)
        db.session.commit()
        return {'message': f'Card {state.state_name} deleted successfully'}
    else:
        return {'error': f'State not found with id {id}'}, 404
