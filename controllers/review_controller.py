from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from models.review import Review, review_schema, reviews_schema
from init import db
import functools


review_bp = Blueprint('review_bp', __name__, url_prefix='/review')


# Route to all reviews
@review_bp.route('/')
def get_all_reviews():
    reviews = Review.query.all()
    return review_schema.dump(reviews)

# Route to a single review


@review_bp.route('/<int:id>')
def get_review(id):
    review = Review.query.get(id)
    if review:
        return review_schema.dump(review)
    else:
        return {'error': f'review not found with id {id}'}, 404

# Route to new review


@review_bp.route('/<int:>id', methods=['POST'])
@jwt_required()
def add_review(id):
    body_data = request.get_json()
    # Create new review model instance
    new_review = Review(
        user_id=body_data.get('user_id'),
        park_id=body_data.get('par_id'),
        rating=body_data.get('rating'),
        comment=body_data.get('comment')
    )
    db.session.add(new_review)
    db.session.commit()
    return {'message': f'review {new_review} created successfully'}, 201

# Delete a review


@review_bp.route('/<int:id>', methods=['DELETE'])
def delete_review(id):
    stmt = db.select(review).filter_by(id=id)
    review = db.session.execute(stmt).scalars().one_or_none()
    if review:
        db.session.delete(review)
        db.session.commit()
        return {'message': f'review {review.review} deleted successfully'}, 200
    else:
        return {'error': f'review not found with id {id}'}, 404