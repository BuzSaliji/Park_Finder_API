from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.sql.expression import func
from models.park import Park, park_schema, parks_schema
from models.review import Review, reviews_schema
from models.address import Address
from models.suburb import Suburb
from models.city import City
from models.state import State
from models.user import User
from init import db
import functools

# Create a blueprint for the park routes
park_bp = Blueprint('park_bp', __name__, url_prefix='/park')

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


# Route to get all parks, with optional filters for state, city, and suburb
@park_bp.route('/')
def get_all_parks():
    # Get state filter from query parameters
    state_name = request.args.get('state')
    # Get city filter from query parameters
    city_name = request.args.get('city')
    # Get suburb filter from query parameters
    suburb_name = request.args.get('suburb')

    # Start building the SQL statement to fetch parks
    stmt = db.select(Park).join(Address, Park.address_id == Address.id).join(
        Suburb, Address.suburb_id == Suburb.id)

    # If a state filter is provided, join with City and State tables and add where clause
    if state_name:
        state_name = state_name.lower()
        stmt = stmt.join(City, Suburb.city_id == City.id)\
            .join(State, City.state_id == State.id)\
            .where(func.lower(State.state_name) == state_name)

    # If a city filter is provided, join with City table and add where clause
    if city_name:
        city_name = city_name.lower()
        stmt = stmt.join(City, Suburb.city_id == City.id)\
            .where(func.lower(City.city_name) == city_name)

    # If a suburb filter is provided, add where clause
    if suburb_name:
        suburb_name = suburb_name.lower()
        stmt = stmt.where(func.lower(Suburb.suburb_name) == suburb_name)

    # Execute the SQL statement and fetch all results
    parks = db.session.execute(stmt).scalars().fetchall()

    # If no parks are found, return an error message
    if not parks:
        return {'error': 'No parks found with the provided filters'}, 404

    # Return the serialized parks
    return parks_schema.dump(parks)

# Route to find parks in a state


@park_bp.route('/state/<int:state_id>')
def get_park_in_state(state_id):
    # Join Park, Address, Suburb, City, and State tables
    stmt = db.select(Park).join(Address).join(Suburb).join(City).join(State)\
        .where(State.id == state_id)
    parks = db.session.scalars(stmt).all()

    # if state was found, returnthe parks in state
    if parks:
        return parks_schema.dump(parks)
    else:
        return {'error': f'State not found with id {state_id}'}, 404

# Route to find parks in a city


@park_bp.route('/city/<int:city_id>')
def get_parks_in_city(city_id):
    # Join Park, Address, Suburb, and City tables
    stmt = db.select(Park).join(Address).join(Suburb).join(City)\
        .where(City.id == city_id)
    parks = db.session.scalars(stmt).all()

    # If city was found, return the parks in city
    if parks:
        return parks_schema.dump(parks)
    else:
        return {'error': f'City not found with id {city_id}'}, 404

# Route to find parks in a suburb


@park_bp.route('/suburb/<int:suburb_id>')
def get_parks_in_suburb(suburb_id):
    # Join Park, Address, and Suburb tables
    stmt = db.select(Park).join(Address).join(Suburb)\
        .where(Suburb.id == suburb_id)
    parks = db.session.scalars(stmt).all()

    # If suburb was found, return the parks in suburb
    if parks:
        return parks_schema.dump(parks)
    else:
        return {'error': f'Suburb not found with id {suburb_id}'}, 404

# Route to search for parks by name


@park_bp.route('/search')
def search_parks():
    # Get search term from query parameters and convert to lowercase
    search_term = request.args.get('search', '').lower()

    # Build the SQL statement to find parks whose names contain the search term
    stmt = db.select(Park).where(func.lower(
        Park.park_name).contains(search_term))

    # Execute the SQL statement and fetch all results
    parks = db.session.execute(stmt).scalars().all()

    # If no parks are found, return an error message
    if not parks:
        return {'error': 'No parks found with the provided search term'}, 404

    # Return the serialized parks
    return parks_schema.dump(parks)


# Route to get all reviews for a specific park


@park_bp.route('/<int:id>/reviews')
def get_park_reviews(id):
    # Build the SQL statement to find reviews for the given park ID
    stmt = db.select(Review).where(Review.park_id == id)

    # Execute the SQL statement and fetch all results
    reviews = db.session.execute(stmt).scalars().all()

    # If no reviews are found, return an error message
    if not reviews:
        return {'error': 'No reviews found for this park'}, 404

    # Return the serialized reviews
    return reviews_schema.dump(reviews)


# Route to get a single park by its ID


@park_bp.route('/<int:id>')
def get_park(id):
    stmt = db.select(Park).filter_by(id=id)  # Find the park in the database
    park = db.session.scalar(stmt)  # Fetch the first result
    # Check if the park was found and either return it or return an error message
    if park:
        return park_schema.dump(park)  # Convert the park to JSON and return it
    else:
        return {'error': f'park not found with id {id}'}, 404

# Route to add a new park


@park_bp.route('/', methods=['POST'])
@jwt_required()  # Require a valid JWT token
def add_park():
    body_data = request.get_json()  # Get the JSON data from the request
    # Check if park with provided name already exists
    park_name = body_data.get('park_name')
    stmt = db.select(Park).where(Park.park_name == park_name)
    existing_park = db.session.execute(stmt).scalars().first()
    if existing_park:
        return {'error': f'Park with name {park_name} already exists'}, 400

    # Continue with creating model instance
    new_park = Park(
        park_name=body_data.get('park_name'),
        description=body_data.get('description'),
        address_id=body_data.get('address_id'),
        user_id=body_data.get('user_id')
    )

    db.session.add(new_park)  # Add the new park to the database
    db.session.commit()  # Save the changes

    return {'message': f'Park {new_park.park_name} created successfully'}, 201


# Route to delete a park


@park_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def delete_park(id):
    stmt = db.select(Park).filter_by(id=id)  # Find the park in the database
    # Fetch the first result or None if not found
    park = db.session.execute(stmt).scalars().one_or_none()
    # Check if the park was found and either delete it or return an error message
    if park:
        db.session.delete(park)  # Delete the park
        db.session.commit()  # Save the changes
        return {'message': f'park {park.park_name} deleted successfully'}, 200
    else:
        return {'error': f'park not found with id {id}'}, 404

# Route to update a park


@park_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require the user to be an admin
def update_one_park(id):
    # Get the JSON data from the request
    body_data = park_schema.load(request.get_json(), partial=True)
    stmt = db.select(Park).filter_by(id=id)  # Find the park in the database
    park = db.session.scalar(stmt)  # Fetch the first result
    # Check if the park was found and either update it or return an error message
    if park:
        park.park_name = body_data.get('park_name') or park.park_name
        park.description = body_data.get('description') or park.description
        db.session.commit()  # Save the changes
        return {
            'message': 'Park updated successfully',
            # Convert the park to JSON and return it
            'park': park_schema.dump(park)
        }, 200
    else:
        return {'error': f'Park not found with id {id}'}, 404
