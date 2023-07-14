from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.address import Address, address_schema, addresses_schema
from models.user import User
from init import db
import functools

address_bp = Blueprint('address_bp', __name__, url_prefix='/address')


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

# Route to all address


@address_bp.route('/')
def get_all_address():
    addresses = Address.query.all()
    return addresses_schema.dump(addresses)


@address_bp.route('/<int:id>')
def get_address(id):
    address = Address.query.get(id)
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
@authorise_as_admin
def delete_address(id):
    stmt = db.select(address).filter_by(id=id)
    address = db.session.execute(stmt).scalars().one_or_none()
    if address:
        db.session.delete(address)
        db.session.commit()
        return {'message': f'address {address.address} deleted successfully'}, 200
    else:
        return {'error': f'address not found with id {id}'}, 404
