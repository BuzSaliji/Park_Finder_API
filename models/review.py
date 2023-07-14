from marshmallow import fields
from sqlalchemy import CheckConstraint
from init import db, ma


class Review(db.Model):
    __tablename__ = 'reviews'

    comment = db.Column(db.String(250))
    rating = db.Column(db.Integer)
    park_id = db.Column(db.Integer, db.ForeignKey(
        'parks.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 10', name='rating_range'),
    )


class ReviewSchema(ma.Schema):
    fields = ('comment', 'rating', 'park_id', 'user_id')
    ordered = True


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
