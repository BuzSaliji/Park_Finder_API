from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.sql.expression import func
from models.address import Address, address_schema, addresses_schema
from models.suburb import Suburb
from models.city import City
from models.state import State
from models.user import User
from init import db
import functools

# Create a blueprint for the park routes
address_bp = Blueprint('address_bp', __name__, url_prefix='/address')

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


@address_bp.route('/')
def get_all_addresses():
    stmt = db.select(Address)
    addresses = db.session.scalars(stmt)
    return addresses_schema.dump(addresses)


@address_bp.route('/<int:id>')
def get_address(id):
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)

    if address:
        return address_schema.dump(address)
    else:
        return {'error': f'state not found with id {id}'}, 404


@address_bp.route('/', methods=['POST'])
@jwt_required()
@authorise_as_admin
def add_address():
    body_data = request.get_json()
    address = Address(
        street_number=body_data.get('street_number'),
        street_name=body_data.get('street_name'),
        postcode=body_data.get('postcode')
    )
    db.session.add(address)
    db.session.commit()
    return address_schema.dump(address), 201


@address_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_address(id):
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)
    if address:
        db.session.delete(address)
        db.session.commit()
        return {'message': f'Address {address.address_id} deleted successfully'}, 200
    else:
        return {'error': f'Address not found with id {id}'}, 404


@address_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_one_address(id):

    body_data = address_schema.load(request.get_json(), partial=True)
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)
    if address:
        address.street_number = body_data.get(
            'street_number') or address.street_number
        address.street_name = body_data.get(
            'street_name') or address.street_name
        address.postcode = body_data.get('postcode') or address.postcode

        db.session.commit()
        return {
            'message': 'Address updated successfully',
            'address': address_schema.dump(address)
        }, 200
    else:
        return {'error': f'Address not found with id {id}'}, 404
