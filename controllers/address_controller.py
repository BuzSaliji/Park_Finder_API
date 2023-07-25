from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.sql.expression import func
from models.address import Address, address_schema, addresses_schema
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

# Route to get all addresses


@address_bp.route('/')
def get_all_addresses():
    stmt = db.select(Address)  # Select all addresses
    addresses = db.session.scalars(stmt)  # Fetch results
    # Convert the results to JSON and return them
    return addresses_schema.dump(addresses)

# Route to get a single address by ID


@address_bp.route('/<int:id>')
def get_address(id):
    # Find an address in the database
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)  # Fetch the first result
    # Check if the address was found and either return it or return an error
    if address:
        return address_schema.dump(address)
    else:
        return {'error': f'state not found with id {id}'}, 404

# Route to add a new address


@address_bp.route('/', methods=['POST'])
@jwt_required()  # Require a valid JWT token
def add_address():
    body_data = request.get_json()  # Get the JSON data from the request)
    address = Address(  # Create a mew address with the data
        street_number=body_data.get('street_number'),
        street_name=body_data.get('street_name'),
        postcode=body_data.get('postcode'),
        suburb_id=body_data.get('suburb_id')
    )
    db.session.add(address)  # Add the new address to the database
    db.session.commit()  # Save the changes
    # Convert the new address to JSON and return it
    return address_schema.dump(address), 201

# Route to delete an address


@address_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require user to be admin
def delete_address(id):
    # Find the address in the database
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)  # Fetch the first result
    # Check if the address was found and either delete it or return an error
    if address:
        db.session.delete(address)
        db.session.commit()
        return {'message': f'Address {address.id} deleted successfully'}, 200
    else:
        return {'error': f'Address not found with id {id}'}, 404


# Route to update an address


@address_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()  # Require a valid JWT token
@authorise_as_admin  # Require user to be admin
def update_one_address(id):
    # Get the JSON data from the request
    body_data = address_schema.load(request.get_json(), partial=True)
    # Find the address in the database
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)  # Fetch the first result
    # Check if the address was found and either update it ofr return an error message
    if address:
        address.street_number = body_data.get(
            'street_number') or address.street_number  # Update address number
        address.street_name = body_data.get(
            'street_name') or address.street_name  # Update address name
        address.postcode = body_data.get(
            'postcode') or address.postcode  # Update address postcode

        db.session.commit()  # Save the changes
        # Convert the updated address to JSON and return it
        return {
            'message': 'Address updated successfully',
            'address': address_schema.dump(address)
        }, 200
    else:
        return {'error': f'Address not found with id {id}'}, 404
