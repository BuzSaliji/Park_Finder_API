from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from models.park import Park, park_schema, parks_schema
from models.address import Address, address_schema
from models.user import User
from init import db
import functools

park_bp = Blueprint('park_bp', __name__, url_prefix='/park')


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

# Route to all Parks


@park_bp.route('/')
def get_all_parks():
    parks = Park.query.all()
    return parks_schema.dump(parks)


@park_bp.route('/<int:id>')
def get_park(id):
    park = Park.query.get(id)
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
@authorise_as_admin
def delete_park(id):
    stmt = db.select(Park).filter_by(id=id)
    park = db.session.execute(stmt).scalars().one_or_none()
    if park:
        db.session.delete(park)
        db.session.commit()
        # Assuming 'name' is an attribute of park
        return {'message': f'park {park.park_name} deleted successfully'}, 200
    else:
        return {'error': f'park not found with id {id}'}, 404
