from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models.park import Park, park_schema, parks_schema
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


@park_bp.route('/', methods=['POST'])
@jwt_required()
def add_park():
    body_data = request.get_json()
    # Create new instance model
    new_park = Park(
        park_name=body_data.get('park_name'),
        description=body_data.get('description'),
        address_id=body_data.get('address_id'),
        user_id=body_data.get('user_id')
    )

    # Add that Park to the new session
    db.session.add(new_park)
    # Commit
    db.session.commit()
    # Respond to the client
    return park_schema.dump(new_park), 201


@park_db.route('/<int:id>', methods=['DELETE'])
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
