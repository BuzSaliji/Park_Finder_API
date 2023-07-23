from init import db, ma
from marshmallow import fields

# Define the User model


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(50), nullable=False,
                         unique=True)  # Unique username
    email = db.Column(db.String(100), nullable=False,
                      unique=True)  # Unique email
    password = db.Column(db.String, nullable=False)  # Password
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag

    # Relationship to the Park model
    parks = db.relationship('Park', back_populates='user')
    # Relationship to the Review model
    reviews = db.relationship('Review', back_populates='user')

# Define the schema for the User model for serialisation


class UserSchema(ma.Schema):
    class Meta:
        # Fields to include in the serialised output
        fields = ('id', 'username', 'email', 'password', 'is_admin')


# Create instances of the schema for single and multiple User objects, excluding the password field
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])
