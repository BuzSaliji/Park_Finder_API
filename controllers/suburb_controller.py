from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.suburb import Suburb, suburb_schema, suburbs_schema
from models.user import User
from init import db
import functools

suburb_bp = Blueprint('suburb_bp', __name__, url_prefix='/suburb')


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

# Route to all suburb


@suburb_bp.route('/')
def get_all_suburbs():
    suburbs = Suburb.query.all()
    return suburbs_schema.dump(suburbs)


@suburb_bp.route('/<int:id>')
def get_suburb(id):
    suburb = Suburb.query.get(id)
    if suburb:
        return suburb_schema.dump(suburb)
    else:
        return {'error': f'suburb not found with id {id}'}, 404

    # Rout to add new suburb


@suburb_bp.route('/', methods=['POST'])
@jwt_required()
def add_suburb():
    body_data = request.get_json()
    # Create new suburb model instance
    new_suburb = Suburb(
        suburb=body_data.get('suburb'),
        city_id=body_data.get('city_id')
    )

    # Add that suburb to the session
    db.session.add(new_suburb)
    # Commit
    db.session.commit()
    # Respond to the client
    return suburb_schema.dump(new_suburb), 201

# Delete suburb


@suburb_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_suburb(id):
    stmt = db.select(suburb).filter_by(id=id)
    suburb = db.session.execute(stmt).scalars().one_or_none()
    if suburb:
        db.session.delete(suburb)
        db.session.commit()
        return {'message': f'suburb {suburb.suburb} deleted successfully'}, 200
    else:
        return {'error': f'suburb not found with id {id}'}, 404
