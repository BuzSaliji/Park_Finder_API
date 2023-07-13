from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.address import Address, address_schema, addresses_schema
from init import db

address_bp = Blueprint('address_bp', __name__, url_prefix='/address')

# Route to all address


@address_bp.route('/')
def get_all_address():
    stmt = db.select(Address)
    address = db.session.scalars(stmt)
    return address_schema.dump(address)


@address_bp.route('/<int:id>')
def get_address(id):
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalars(stmt)
    if address:
        return address_schema.dump(address)
    else:
        return {'error': f'address not found with id {id}'}, 404

    # Rout to add new address


@address_bp.route('/', methods=['POST'])
@jwt_required()
def add_address():
    body_data = request.get_json()
    # Create new address model instance
    new_address = Address(
        address=body_data.get('address'),
        city_id=body_data.get('city_id')
    )

    # Add that Address to the session
    db.session.add(new_address)
    # Commit
    db.session.commit()
    # Respond to the client
    return address_schema.dump(new_address), 201


@address_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    stmt = db.select(address).filter_by(id=id)
    address = db.session.execute(stmt).scalars().one_or_none()
    if address:
        db.session.delete(address)
        db.session.commit()
        return {'message': f'address {address.address} deleted successfully'}, 200
    else:
        return {'error': f'address not found with id {id}'}, 404
