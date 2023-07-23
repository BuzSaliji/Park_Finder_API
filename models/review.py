from marshmallow import fields
from sqlalchemy import CheckConstraint
from init import db, ma

# Define the Review model


class Review(db.Model):
    __tablename__ = 'reviews'

    comment = db.Column(db.String(250))  # Comment of the review
    rating = db.Column(db.Integer)  # Rating of the review
    park_id = db.Column(db.Integer, db.ForeignKey(
        'park.id'), primary_key=True)  # Foreign key to the Park table
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)  # Foreign key to the Users table

    # Relationship to the User model
    user = db.relationship('User', back_populates='reviews')
    # Relationship to the Park model
    park = db.relationship('Park', back_populates='reviews')

    __table_args__ = (
        # Rating must be between 1 and 10
        CheckConstraint('rating >= 1 AND rating <= 10', name='rating_range'),
    )

# Define the schema for the Review model for serialisation


class ReviewSchema(ma.Schema):
    class Meta:
        # Fields to include in the serialised output
        fields = ('comment', 'rating', 'park_id', 'user_id')
        ordered = True  # Order the fields in the output


# Create instances of the schema for single and multiple Review objects
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
