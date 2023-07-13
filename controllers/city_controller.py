from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.city import City, city_schema, cities_schema
from init import db

city_bp = Blueprint('city_bp', __name__, url_prefix='/city')

# Route to get all cities


@city_bp.route('/')
def get_all_city():
    cities = City.query.all()
    return cities_schema.dump(cities)


@city_bp.route('/<int:id>')
def get_city(id):
    city = City.query.get(id)
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
def delete_city(id):
    stmt = db.select(City).filter_by(id=id)
    city = db.session.scalar(stmt)
    if city:
        db.session.delete(city)
        db.session.commit()
        return {'message': f'City {city.city_name} deleted successfully'}, 200
    else:
        return {'error': f'City not found with id {id}'}, 404
