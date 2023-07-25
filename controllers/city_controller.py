from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.city import City, city_schema, cities_schema
from models.suburb import Suburb, suburb_schema, suburbs_schema
from models.user import User
from init import db
import functools

# Create a blueprint for the city routes
city_bp = Blueprint('city_bp', __name__, url_prefix='/city')

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

# Route to get all cities


@city_bp.route('/')
def get_all_city():
    stmt = db.select(City)  # Select all cities
    cities = db.session.scalars(stmt)  # Fetch the results
    # Convert the results to JSON and return them
    return cities_schema.dump(cities)

# Route to get a single city by its ID


@city_bp.route('/<int:id>')
def get_city(id):
    stmt = db.select(City).filter_by(id=id)  # Find the city in the database
    city = db.session.scalar(stmt)  # Fetch the first result
    # Check if the city was found and either return it or return an error message
    if city:
        return city_schema.dump(city)
    else:
        return {'error': f'City not found with id {id}'}, 404

# Route to find subrubs in a city


@city_bp.route('/<int:city_id>/suburbs')
def get_suburbs_in_city(city_id):
    # Find city in the database
    stmt = db.select(City).filter_by(id=city_id)
    city = db.session.scalar(stmt)

    # If the city was found, return the suburbs in the city
    if city:
        suburbs = city.suburbs
        return suburbs_schema.dump(suburbs)
    else:
        return {'error': f'City not found with id {city_id}'}, 404

# Route to add a new city


@city_bp.route('/', methods=['POST'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def add_city():
    try:
        body_data = request.get_json()  # Get the JSON data from the request
        city = City(  # Create a new city with the data
            city_name=body_data.get('city_name'),
            state_id=body_data.get('state_id')
        )
        db.session.add(city)  # Add the new city to the database
        db.session.commit()  # Save the changes
        # Convert the new city to JSON and return it
        return {'message': f'City {city.city_name} was successfully created'}, 201
    except IntegrityError as err:
        db.session.rollback()
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {'error': 'City name already in use'}, 400
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {'error': f'The {err.orig.diag.column_name} field is required'}, 409


# Route to delete a city
@city_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def delete_city(id):
    stmt = db.select(City).filter_by(id=id)  # Find the city in the database
    city = db.session.scalar(stmt)  # Fetch the first result
    # Check if the city was found and either delete it or return an error message
    if city:
        db.session.delete(city)  # Delete the city
        db.session.commit()  # Save the changes
        return {'message': f'City {city.city_name} deleted successfully'}, 200
    else:
        return {'error': f'City not found with id {id}'}, 404

# Route to update a city


@city_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def update_one_city(id):
    # Get the JSON data from the request
    body_data = city_schema.load(request.get_json(), partial=True)
    stmt = db.select(City).filter_by(id=id)  # Find the city in the database
    city = db.session.scalar(stmt)  # Fetch the first result
    # Check if the city was found and either update it or return an error message
    if city:
        city.city_name = body_data.get(
            'city_name') or city.city_name  # Update the city's name
        db.session.commit()  # Save the changes
        # Convert the updated city to JSON and return it
        return {'message': 'City updated successfully', 'city': city_schema.dump(city)}, 200
    else:
        return {'error': f'City not found with id {id}'}, 404
