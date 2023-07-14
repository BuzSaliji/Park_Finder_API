from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.state import State, state_schema, states_schema
from models.user import User
from init import db
import functools

state_bp = Blueprint('state_bp', __name__, url_prefix='/state')


def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to perform delete'}, 403

    return wrapper

# Route to all States


@state_bp.route('/')
def get_all_states():
    stmt = db.select(State)
    states = db.session.scalars(stmt)
    return states_schema.dump(states)

# Route to a single State


@state_bp.route('/<int:id>')
def get_state(id):
    stmt = db.select(State).filter_by(id=id)
    state = db.session.scalar(stmt)
    if state:
        return state_schema.dump(state)
    else:
        return {'error': f'State not found with id {id}'}, 404

# Route to create a State


@state_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def add_state():
    body_data = request.get_json()
    state = State(
        state_name=body_data.get('state_name')
    )

    db.session.add(state)
    db.session.commit()

    return state_schema.dump(state), 201

# Route to delete a state


@state_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_state(id):
    stmt = db.select(State).filter_by(id=id)
    state = db.session.scalar(stmt)
    if state:
        db.session.delete(state)
        db.session.commit()
        return {'message': f'State {state.state_name} deleted successfully'}, 200
    else:
        return {'error': f'State not found with id {id}'}, 404
