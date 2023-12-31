from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.state import State, state_schema, states_schema
from models.city import City, city_schema, cities_schema
from models.user import User
from init import db
import functools

# Create a blueprint for the state routes
state_bp = Blueprint('state_bp', __name__, url_prefix='/state')

# Define a decorator to check if a user is an admin


def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()  # Get the user ID from the JWT token
        # Find the user in the database
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)  # Fetch the first result
        # Check if the user is an admin and either execute the function or return an error message
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            return {'error': 'Not authorised to perform delete'}, 403
    return wrapper

# Route to get all states


@state_bp.route('/')
def get_all_states():
    stmt = db.select(State)  # Select all states
    states = db.session.scalars(stmt)  # Fetch the results
    # Convert the results to JSON and return them
    return states_schema.dump(states)

# Route to get a single state by its ID


@state_bp.route('/<int:id>')
def get_state(id):
    stmt = db.select(State).filter_by(id=id)  # Find the state in the database
    state = db.session.scalar(stmt)  # Fetch the first result
    # Check if the state was found and either return it or return an error message
    if state:
        # Convert the state to JSON and return it
        return state_schema.dump(state)
    else:
        return {'error': f'State not found with id {id}'}, 404


# Route to find cities in a state

@state_bp.route('/<int:state_id>/cities')
def get_cities_in_state(state_id):
    # Find the state in the database
    stmt = db.select(State).filter_by(id=state_id)
    state = db.session.scalar(stmt)

    # If the state was found, return the cities in the state
    if state:
        cities = state.cities
        return cities_schema.dump(cities)
    else:
        return {'error': f'State not found with id {state_id}'}, 404


# Route to add a new state


@state_bp.route('/', methods=['POST'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def add_state():
    try:
        body_data = request.get_json()  # Get the JSON data from the request
        state = State(  # Create a new state with the data
            state_name=body_data.get('state_name')
        )
        db.session.add(state)  # Add the new state to the database
        db.session.commit()  # Save the changes
        # Convert the new state to JSON and return it
        return {'message': f'State {state.state_name} was successfully created'}, 201
    except IntegrityError as err:
        db.session.rollback()
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'State name already in use'}, 400
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} field is required'}, 409


# Route to delete a state


@state_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def delete_state(id):
    stmt = db.select(State).filter_by(id=id)  # Find the state in the database
    state = db.session.scalar(stmt)  # Fetch the first result
    # Check if the state was found and either delete it or return an error message
    if state:
        db.session.delete(state)  # Delete the state
        db.session.commit()  # Save the changes
        return {'message': f'State {state.state_name} deleted successfully'}, 200
    else:
        return {'error': f'State not found with id {id}'}, 404

# Route to update a state


@state_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def update_one_state(id):
    # Get the JSON data from the request
    body_data = state_schema.load(request.get_json(), partial=True)
    stmt = db.select(State).filter_by(id=id)  # Find the state in the database
    state = db.session.scalar(stmt)  # Fetch the first result
    # Check if the state was found and either update it or return an error message
    if state:
        state.state_name = body_data.get(
            'state_name') or state.state_name  # Update the state's name
        db.session.commit()  # Save the changes
        # Convert the updated state to JSON and return it
        return {
            'message': 'State updated successfully',
            'state': state_schema.dump(state)
        }, 200
    else:
        return {'error': f'State not found with id {id}'}, 404
