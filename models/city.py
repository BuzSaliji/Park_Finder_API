from init import db, ma
from marshmallow import fields, validates, ValidationError

# Define the City model


class City(db.Model):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    city_name = db.Column(db.String(50), nullable=False)  # Name of the city

    state_id = db.Column(db.Integer, db.ForeignKey(
        'state.id'), nullable=False)  # Foreign key to the State table

    # Relationship to the State model
    state = db.relationship('State', back_populates='cities')
    # Relationship to the Suburb model
    suburbs = db.relationship('Suburb', back_populates='city')

# Define the schema for the City model for serialisation


class CitySchema(ma.Schema):
    state = fields.Nested('StateSchema', exclude=[
                          'cities'])  # Nested State schema
    suburbs = fields.Nested('SuburbSchema', exclude=[
                            'city'], many=True)  # Nested Suburb schema

    @validates('city_name')  # Validation for the city_name field
    def validate_city_name(self, value):
        # Raise a validation error if the city name is not alphabetic
        if not value.isalpha():
            raise ValidationError(
                'city name should only contain alphabetic characters')

    class Meta:
        # Fields to include in the serialised output
        fields = ('id', 'city_name', 'state')
        ordered = True  # Order the fields in the output


# Create instances of the schema for single and multiple City objects
city_schema = CitySchema()
cities_schema = CitySchema(many=True)
