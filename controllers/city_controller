from flask import Blueprint, request, jsonify
from models.city import City, city_schema, cities_schema
from init import db

city_bp = Blueprint('city_bp', __name__)

# Route to get all cities


@city_bp.route('/cities', methods=['GET'])
def get_all_cities():
    all_cities = City.query.all()
    result = cities_schema.dump(all_cities)
    return jsonify(result)


# Route to add new city
@city_bp.route('/city', methods=['POST'])
def add_city():
    city_name = request.json['city_name']
    new_city = City(city_name=city_name)

    db.session.add(new_city)
    db.session.commit()

    return city_schema.jsonify(new_city)
