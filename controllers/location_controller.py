from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.location import Location, location_schema, locations_schema
from init import db

location_bp = Blueprint('city_bp', __name__, url_prefix='/location')

# Route to all locations


@location_bp.route('/')
def get_all_location():
    stmt = db.select(Location)
    locations = db.session.scalars(stmt)
    return location_schema.dump(locations)


@location_bp.route('/<int:id>')
def get_location(id):
    stmt = db.select(Location).filter_by(id=id)
    location = db.session.scalars(stmt)
    if location:
        return location_schema.dump(location)
    else:
        return {'error': f'Location not found with id {id}'}, 404

    # Rout to add new location


@location_bp.route('/', methods=['POST'])
@jwt_required
def add_location(id):
    body_data = request.get_json()
    # Create new Location model instance
    location = Location(
        address=body_data.get('address'),
        city_name=body_data.get('city_name')
    )

    # Add that Address to the session
    db.session.add(location)
    # Commit
    db.session.commit()
    # Respond to the client
    return location_schema.dump(location), 201


@location_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_location(id):
    stmt = select(Location).filter_by(id=id)
    location = db.session.execute(stmt).scalars().one_or_none()
    if location:
        db.session.delete(location)
        db.session.commit()
        return {'message': f'Location {location.address} deleted successfully'}, 200
    else:
        return {'error': f'Location not found with id {id}'}, 404
