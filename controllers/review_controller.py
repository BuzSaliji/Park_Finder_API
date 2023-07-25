from models.review import Review
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.review import Review, review_schema, reviews_schema
from models.user import User, user_schema, users_schema
from models.park import Park, park_schema, parks_schema
from init import db
from sqlalchemy import and_
import functools

# Create a blueprint for the review routes
review_bp = Blueprint('review_bp', __name__, url_prefix='/review')


# Route to get all reviews with optional filtering


@review_bp.route('/')
def get_all_reviews():
    # Get filter parameters from the request
    min_rating = request.args.get('min_rating')
    park_id = request.args.get('park_id')
    user_id = request.args.get('user_id')

    # Initialize a select statement for reviews
    stmt = db.select(Review)

    # Apply filters to the select statement
    if min_rating is not None:
        stmt = stmt.where(Review.rating >= min_rating)
    if park_id is not None:
        stmt = stmt.where(Review.park_id == park_id)
    if user_id is not None:
        stmt = stmt.where(Review.user_id == user_id)

    # Execute the statement and get all results
    reviews = db.session.execute(stmt).scalars().all()

    # Return the serialized results
    return reviews_schema.dump(reviews)

# Route to get reviews by a user


@review_bp.route('/user/<int:user_id>')
def get_review_by_user(user_id):
    # Fin the user in the database
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    # If the user was found, return the reviews by the user
    if user:
        reviews = user.reviews
        return reviews_schema.dump(reviews)
    else:
        return {'error': f'User not found with the id {user_id}'}, 404

# Route to get all reviews for a specific park


@review_bp.route('/park/<int:park_id>')
def get_review_by_park(park_id):
    # Find the park in the database
    stmt = db.select(Park).filter_by(id=park_id)
    park = db.session.scalar(stmt)

    # If the park was found, retrurn the reviews for the park
    if park:
        reviews = park.reviews
        return reviews_schema.dump(reviews)
    else:
        return {'error': f'Park not found with id {park_id}'}, 404

# Route to get a single review by a user for a park


@review_bp.route('/<int:user_id>/<int:park_id>')
def get_review(user_id, park_id):
    # Initialize a select statement for the specific review
    stmt = db.select(Review).where(
        (Review.user_id == user_id) & (Review.park_id == park_id))

    # Execute the statement and get the first result
    review = db.session.scalar(stmt)

    # If the review exists, return the serialized review, else return an error message
    if review:
        return review_schema.dump(review)
    else:
        return {'error': f'Review not found for user_id {user_id} and park_id {park_id}'}, 404


# Route to add a new review
@review_bp.route('/', methods=['POST'])
@jwt_required()  # Requires a valid access token in the request header
def add_review():
    # Get the request data
    body_data = request.get_json()
    rating = body_data.get('rating')
    # Check if rating is a string and convert it to an integer
    if isinstance(rating, str):
        try:
            rating = int(rating)
        except ValueError:
            return {'error': 'Rating must be a number between 1 and 10'}, 400

    # Check the rating range
    if rating is None or rating < 1 or rating > 10:
        return {'error': 'Rating must be between 1 and 10'}, 400

    # Check if the user has already reviewed the park
    user_id = body_data.get('user_id')
    park_id = body_data.get('park_id')
    stmt = db.select(Review).where(
        and_(Review.user_id == user_id, Review.park_id == park_id))
    existing_review = db.session.execute(stmt).scalars().first()
    if existing_review:
        return {'error': 'You have already reviewed this park'}, 400

    # Create the new review object
    new_review = Review(
        user_id=body_data.get('user_id'),
        park_id=body_data.get('park_id'),
        rating=rating,
        comment=body_data.get('comment')
    )

    # Add the new review to the session and commit it to the database
    db.session.add(new_review)
    db.session.commit()

    # Return a success message
    return {'message': f'review {new_review} created successfully'}, 201

# Route to delete a review


@review_bp.route("/<int:user_id>/<int:park_id>", methods=["DELETE"])
@jwt_required()  # Requires a valid access token in the request header
def delete_review(user_id, park_id):
    # Get the identity of the current user
    current_user_id = get_jwt_identity()

    # Fetch the review to be deleted
    stmt = db.select(Review).where(
        and_(Review.user_id == user_id, Review.park_id == park_id))
    review = db.session.execute(stmt).scalars().first()

    # If the review exists, delete it, else return an error message
    if review:
        # Check if the current user is the owner of the review or an admin
        if str(review.user_id) != current_user_id:
            stmt = db.select(User).filter_by(id=current_user_id)
            current_user = db.session.scalar(stmt)
            if not current_user.is_admin:
                return {'error': 'Not authorized to perform delete'}, 403

        # Delete the review
        db.session.delete(review)
        db.session.commit()

        # Return a success message
        return {'message': 'Review deleted successfully'}, 200
    else:
        return {'error': 'Review not found'}, 404


# Route to update a review
@review_bp.route('/<int:user_id>/<int:park_id>', methods=['PUT', 'PATCH'])
@jwt_required()  # Requires a valid access token in the request header
def update_one_review(user_id, park_id):
    # Get the request data
    body_data = review_schema.load(request.get_json(), partial=True)

    # Fetch the review to be updated
    stmt = db.select(Review).where(
        and_(Review.user_id == user_id, Review.park_id == park_id))
    review = db.session.execute(stmt).scalars().first()

    # If the review exists, update it, else return an error message
    if review:
        # Check if the current user is the owner of the review
        if str(review.user_id) != get_jwt_identity():
            return {'error': 'Only the owner of the review can edit'}, 403

        # Update the review data
        review.rating = body_data.get('rating') or review.rating
        review.comment = body_data.get('comment') or review.comment

        # Commit the changes to the database
        db.session.commit()

        # Return a success message and the updated review data
        return {
            'message': 'Review updated successfully',
            'review': review_schema.dump(review)
        }, 200
    else:
        return {'error': f'Review not found for user id {user_id} and park id {park_id}'}, 404
