from init import db, ma
from marshmallow import validates, ValidationError, fields
from marshmallow.validate import Range, Length
from sqlalchemy import CheckConstraint


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

    comment = fields.String(validate=Length(max=250))  # Comment of the review
    rating = fields.Integer(validate=Range(
        min=1, max=10))  # Rating of the review

    user = fields.Nested('UserSchema', only=['name'])
    park = fields.Nested('ParkSchema', only=['park_name'])

    def validate_comment(self, value):
        if not isinstance(value, str):
            raise ValidationError("Comment must be a string")
        if len(value.strip()) == 0:
            raise ValidationError("Comment must not be empty")

    ...

    class Meta:
        # Fields to include in the serialised output
        fields = ('comment', 'rating', 'park_id', 'user_id')
        ordered = True  # Order the fields in the output


# Create instances of the schema for single and multiple Review objects
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
