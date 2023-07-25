from init import db, ma
from marshmallow import fields, validates, ValidationError

# Define the State model


class State(db.Model):
    __tablename__ = 'state'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    state_name = db.Column(db.String(50), unique=True,
                           nullable=False)  # Name of the state

    # Relationship to the City model
    cities = db.relationship('City', back_populates='state')

# Define the schema for the State model for serialisation


class StateSchema(ma.Schema):

    @validates('state_name')  # Validation for the state_name field
    def validate_state_name(self, value):
        # Raise a validation error if the state name is not alphabetic
        if not value.replace(" ", "").isalpha:
            raise ValidationError(
                'State name should only contain alphabetic characters and spaces')

    class Meta:
        # Fields to include in the serialised output
        fields = ('id', 'state_name')
        ordered = True  # Order the fields in the output


# Create instances of the schema for single and multiple State objects
state_schema = StateSchema()
states_schema = StateSchema(many=True)
