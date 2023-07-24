from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.city import City, city_schema, cities_schema
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

# Define a route to get all cities


@city_bp.route('/')
def get_all_city():
    stmt = db.select(City)  # Select all cities
    cities = db.session.scalars(stmt)  # Fetch the results
    # Convert the results to JSON and return them
    return cities_schema.dump(cities)

# Define a route to get a single city by its ID


@city_bp.route('/<int:id>')
def get_city(id):
    stmt = db.select(City).filter_by(id=id)  # Find the city in the database
    city = db.session.scalar(stmt)  # Fetch the first result
    # Check if the city was found and either return it or return an error message
    if city:
        return {
            'message': 'City updated successfully',
            # Convert the city to JSON and return it
            'city': city_schema.dump(city)
        }, 200
    else:
        return {'error': f'City not found with id {id}'}, 404

# Define a route to add a new city


@city_bp.route('/', methods=['POST'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def add_city():
    body_data = request.get_json()  # Get the JSON data from the request
    city = City(  # Create a new city with the data
        city_name=body_data.get('city_name'),
        state_id=body_data.get('state_id')
    )
    db.session.add(city)  # Add the new city to the database
    db.session.commit()  # Save the changes
    # Convert the new city to JSON and return it
    return city_schema.dump(city), 201

# Define a route to delete a city


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

# Define a route to update a city


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
        return city_schema.dump(city)
    else:
        return {'error': f'City not found with id {id}'}, 404
