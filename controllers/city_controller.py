from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.city import City, city_schema, cities_schema
from models.user import User
from init import db
import functools

city_bp = Blueprint('city_bp', __name__, url_prefix='/city')


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

# Route to get all cities


@city_bp.route('/')
def get_all_city():
    stmt = db.select(City)
    cities = db.session.scalars(stmt)
    return cities_schema.dump(cities)

# Route to a single City


@city_bp.route('/<int:id>')
def get_city(id):
    stmt = db.select(City).filter_by(id=id)
    city = db.session.scalar(stmt)
    if city:
        return city_schema.dump(city)
    else:
        return {'error': f'City not found with id {id}'}, 404

# Route to add new city


@city_bp.route('/', methods=['POST'])
@jwt_required()
def add_city():
    body_data = request.get_json()
    # Create a new City model instance
    city = City(
        city_name=body_data.get('city_name'),
        state_id=body_data.get('state_id')
    )

    # Add that city to the session
    db.session.add(city)
    # Commit
    db.session.commit()
    # Respond to he client
    return city_schema.dump(city), 201
# Route to delete city


@city_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_city(id):
    stmt = db.select(City).filter_by(id=id)
    city = db.session.scalar(stmt)
    if city:
        db.session.delete(city)
        db.session.commit()
        return {'message': f'City {city.city_name} deleted successfully'}, 200
    else:
        return {'error': f'City not found with id {id}'}, 404


@city_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_one_city(id):
    body_data = city_schema.load(request.get_json(), partial=True)
    stmt = db.select(City).filter_by(id=id)
    city = db.session.scalar(stmt)
    if city:
        city.city_name = body_data.get('city_name') or city.city_name
        db.session.commit()
        return city_schema.dump(city)
    else:
        return {'error': f'City not found with id {id}'}, 404
