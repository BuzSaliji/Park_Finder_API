from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.city import City, city_schema, cities_schema
from init import db

city_bp = Blueprint('city_bp', __name__)

# Route to get all cities


@city_bp.route('/cities', methods=['GET'])
@jwt_required()
def get_all_cities():
    all_cities = City.query.all()
    result = cities_schema.dump(all_cities)
    return jsonify(result)


# Route to add new city
@city_bp.route('/city', methods=['POST'])
@jwt_required()
def add_city():
    data = request.get_json()  # This is where the data from the POST request is coming from

    new_city = City(city_name=data['city_name'], state_id=data['state_id'])
    db.session.add(new_city)
    db.session.commit()

    return city_schema.dump(new_city), 201

# Route to delete city


@city_bp.route('/city/<id>', methods=['DELETE'])
@jwt_required()
def delete_city(id):
    current_user = current_identity
    if current_user.is_admin:
        city = City.query.get(id)
        if city is None:
            return jsonify({"error": "City not found"}), 404

        db.session.delete(city)
        db.session.commit()

        return city_schema.jsonify(city)
    else:
        return jsonify({"error": "Permission denied"}), 403
