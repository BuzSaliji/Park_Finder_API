from init import db, ma
from marshmallow import fields, validates, ValidationError

# Define the Park model


class Park(db.Model):
    __tablename__ = "park"

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    park_name = db.Column(db.String(50), nullable=False)  # Name of the park
    # Description of the park
    description = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(250), nullable=False)  # Address of the park
    address_id = db.Column(db.Integer, db.ForeignKey(
        'address.id'), nullable=False)  # Foreign key to the Address table
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)  # Foreign key to the Users table

    # Relationship to the Address model
    address = db.relationship('Address', back_populates='park', uselist=False)
    # Relationship to the User model
    user = db.relationship('User', back_populates='parks')
    # Relationship to the Review model
    reviews = db.relationship('Review', back_populates='park')

# Define the schema for the Park model for serialisation


class ParkSchema(ma.Schema):

    # Nested User schema
    user = fields.Nested('UserSchema', exclude=['user'])
    address = fields.Nested('AddressSchema', only=[
                            'street_number', 'street_name', 'postcode'])

    @validates('park_name')
    def validate_park_name(self, value):
        if not value.replace(" ", "").isalpha():
            raise ValidationError(
                'Park name should only contain alphabetic characters and spaces')

    class Meta:
        # Fields to include in the serialised output
        fields = ('id', 'park_name',  'description',
                  'user_id', 'address_id', 'address',)
        ordered = True  # Order the fields in the output


# Create instances of the schema for single and multiple Park objects
park_schema = ParkSchema()
parks_schema = ParkSchema(many=True)
