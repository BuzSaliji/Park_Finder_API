from init import db, ma
from marshmallow import fields, validates, ValidationError

# Define the Suburb model


class Suburb(db.Model):
    __tablename__ = "suburb"

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    suburb_name = db.Column(
        db.String(50), nullable=False)  # Name of the suburb
    city_id = db.Column(db.Integer, db.ForeignKey(
        'city.id'), nullable=False)  # Foreign key to the City table

    # Relationship to the City model
    city = db.relationship('City', back_populates='suburbs')
    # Relationship to the Park model
    parks = db.relationship('Park', back_populates='suburb')

# Define the schema for the Suburb model for serialisation


class SuburbSchema(ma.Schema):
    city = fields.Nested('CitySchema', exclude=[
                         'cities'])  # Nested City schema

    @validates('suburb_name')  # Validation for the suburb_name field
    def validate_suburb_name(self, value):
        # Raise a validation error if the suburb name is not alphabetic
        if not value.isalpha():
            raise ValidationError(
                'Suburb name should only contain alphabetic characters')

    class Meta:
        # Fields to include in the serialised output
        fields = ('id', 'suburb_name', 'city_id')
        ordered = True  # Order the fields in the output


# Create instances of the schema for single and multiple Suburb objects
suburb_schema = SuburbSchema()
suburbs_schema = SuburbSchema(many=True)
