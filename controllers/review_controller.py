from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from models.review import Review, review_schema, reviews_schema
from models.user import User
from init import db
import functools


review_bp = Blueprint('review_bp', __name__, url_prefix='/review')


# Route to all reviews
@review_bp.route('/')
def get_all_reviews():
    stmt = db.select(Review)
    result = db.session.execute(stmt)
    reviews = result.scalars().all()
    return {"reviews": [review_schema.dump(review) for review in reviews]}


# Route to a single review


@review_bp.route('/<int:user_id>/<int:park_id>')
def get_review(user_id, park_id):
    stmt = db.select(Review).where(
        (Review.user_id == user_id) & (Review.park_id == park_id))
    review = db.session.scalar(stmt)
    if review:
        return review_schema.dump(review)
    else:
        return {'error': f'Review not found for user_id {user_id} and park_id {park_id}'}, 404


# Route to new review


@review_bp.route('/', methods=['POST'])
@jwt_required()
def add_review():
    body_data = request.get_json
    # Validate the rating
    rating = body_data.get('rating')
    if rating is None or rating < 1 or rating > 10:
        return {'error': 'Rating must be between 1 and 10'}, 400

    # Continue with creating model instance
    new_review = Review(
        user_id=body_data.get('user_id'),
        park_id=body_data.get('park_id'),
        rating=rating,
        comment=body_data.get('comment')
    )

    db.session.add(new_review)
    db.session.commit()

    return {'message': f'review {new_review} created successfully'}, 201

# Delete a review


@review_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    current_user_id = get_jwt_identity()
    stmt = db.select(Review).filter_by(id=id)
    review = db.session.scalar(stmt)
    if review:
        if str(review.user_id) != current_user_id:
            stmt = db.select(User).filter_by(id=current_user_id)
            current_user = db.session.scalar(stmt)
            if not current_user.is_admin:
                return {'error': 'Not authorised to perform delete'}, 403
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Review with id {id} deleted successfully'}, 200
    else:
        return {'error': f'Review not found with id {id}'}, 404


# Route to update a review


@review_bp.route('/<int:user_id>/<int:park_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_review(id):
    body_data = review_schema.load(request.get_json(), partial=True)
    stmt = db.select(Review).filter_by(id=id)
    review = db.session.scalar(stmt)
    if review:
        if str(review.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of the review can edit'}, 403
        review.rating = body_data.get('rating') or review.rating
        review.comment = body_data.get('comment') or review.comment
        db.session.commit()
        return review_schema.dump(review)
    else:
        return {'error': f'Review not found with id {id}'}, 404
