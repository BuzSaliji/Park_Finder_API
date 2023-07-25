from init import db, ma
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Length, Range

# Define the Address model


class Address(db.Model):
    __tablename__ = "address"  # Define the name of the table in the database

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    street_number = db.Column(db.Integer)  # Street number field
    # Street name field, must not be null
    street_name = db.Column(db.String(150), nullable=False)
    # Postcode field, must not be null
    postcode = db.Column(db.Integer, nullable=False)
    suburb_id = db.Column(db.Integer, db.ForeignKey(
        'suburb.id'), nullable=False)  # Foreign key reference to the suburb

    # Define a relationship with the Suburb model
    suburb = db.relationship('Suburb', back_populates='addresses')

    # Define a one-to-one relationship with the Park model
    park = db.relationship('Park', back_populates='address', uselist=False)


# Define the schema for the Address model for serialisation
class AddressSchema(ma.Schema):
    street_number = fields.Integer(required=True, validate=Range(
        min=1, error="Street number must be at least 1"))
    street_name = fields.String(required=True, validate=Length(
        min=2, error='Street name must be at least 2 characters long'))
    postcode = fields.Integer(required=True, validate=Range(
        min=1000, max=9999, error="Postcode must be a 4-digit number"))

    # Define a nested field for the suburb
    suburb = fields.Nested('SuburbSchema', only=['suburb_name'])

    class Meta:
        fields = ('id', 'street_number', 'street_name',
                  'postcode', 'suburb_id', 'suburb')  # Fields to be included in the serialised data
        ordered = True  # Order the fields in the serialised data

    # Define a custom validation for the street_name field
    @validates('street_name')
    def validate_street_name(self, value):
        if not value.replace(" ", "").isalpha():
            raise ValidationError(
                'Street name should only contain alphabetic characters and spaces')


# Create instances of the schema for single and multiple addresses
address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)
