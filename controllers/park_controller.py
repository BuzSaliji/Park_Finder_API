from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from models.park import Park, park_schema, parks_schema
from models.address import Address, address_schema
from init import db

park_bp = Blueprint('park_bp', __name__, url_prefix='/park')

# Route to all Parks


@park_bp.route('/')
def get_all_parks():
    stmt = db.select(Park)
    park = db.session.scalars(stmt)
    return park_schema.dump(park)


@park_bp.route('/<int:id>')
def get_park(id):
    stmt = db.select(Park).filter_by(id=id)
    park = db.session.scalars(stmt)
    if park:
        return park_schema.dump(park)
    else:
        return {'error': f'park not found with id {id}'}, 404

# Route to new park


@park_bp.route('/park', methods=['POST'])
@jwt_required()
def add_park():
    data = request.get_json()

    # create a new address object
    new_address = Address(
        address=data['address'],
        city_id=data['city_id'],
    )
    db.session.add(new_address)
    db.session.flush()  # This assigns an id to the new address object

    # create a new park object
    new_park = Park(
        park_name=data['park_name'],
        description=data['description'],
        address_id=new_address.id,  # use the id of the just-created address
        user_id=data['user_id']
    )
    db.session.add(new_park)
    db.session.commit()

    return {'message': f'Park {new_park.park_name} created successfully'}, 201


@park_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_park(id):
    stmt = db.select(park).filter_by(id=id)
    park = db.session.execute(stmt).scalars().one_or_none()
    if park:
        db.session.delete(park)
        db.session.commit()
        return {'message': f'park {park.park} deleted successfully'}, 200
    else:
        return {'error': f'park not found with id {id}'}, 404
