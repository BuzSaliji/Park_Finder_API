from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.suburb import Suburb, suburb_schema, suburbs_schema
from models.user import User
from init import db
import functools

# Create a blueprint for the suburb routes
suburb_bp = Blueprint('suburb_bp', __name__, url_prefix='/suburb')

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

# Define a route to get all suburbs


@suburb_bp.route('/')
def get_all_suburbs():
    stmt = db.select(Suburb)  # Select all suburbs
    suburbs = db.session.scalars(stmt)  # Fetch the results
    # Convert the results to JSON and return them
    return suburbs_schema.dump(suburbs)

# Define a route to get a single suburb by its ID


@suburb_bp.route('/<int:id>')
def get_suburb(id):
    # Find the suburb in the database
    stmt = db.select(Suburb).filter_by(id=id)
    suburb = db.session.scalar(stmt)  # Fetch the first result
    # Check if the suburb was found and either return it or return an error message
    if suburb:
        # Convert the suburb to JSON and return it
        return suburb_schema.dump(suburb)
    else:
        return {'error': f'suburb not found with id {id}'}, 404

# Define a route to add a new suburb


@suburb_bp.route('/', methods=['POST'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def add_suburb():
    body_data = request.get_json()  # Get the JSON data from the request
    new_suburb = Suburb(  # Create a new suburb with the data
        suburb_name=body_data.get('suburb'),
        city_id=body_data.get('city_id')
    )
    db.session.add(new_suburb)  # Add the new suburb to the database
    db.session.commit()  # Save the changes
    # Convert the new suburb to JSON and return it
    return suburb_schema.dump(new_suburb), 201

# Define a route to delete a suburb


@suburb_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def delete_suburb(id):
    # Find the suburb in the database
    stmt = db.select(Suburb).filter_by(id=id)
    # Fetch the first result or None if not found
    suburb = db.session.execute(stmt).scalars().one_or_none()
    # Check if the suburb was found and either delete it or return an error message
    if suburb:
        db.session.delete(suburb)  # Delete the suburb
        db.session.commit()  # Save the changes
        return {'message': f'suburb {suburb.suburb_name} deleted successfully'}, 200
    else:
        return {'error': f'suburb not found with id {id}'}, 404
