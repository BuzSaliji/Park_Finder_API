from init import db, ma
from marshmallow import fields, validates, ValidationError


class State(db.Model):
    __tablename__ = 'state'

    id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(50), nullable=False)

    cities = db.relationship('City', back_populates='state')


class StateSchema(ma.Schema):
    cities = fields.Nested('CitySchema', many=True, exclude=['state'])

    @validates('state_name')
    def validate_state_name(self, value):
        if not value.isalpha():
            raise ValidationError(
                'State name should only contain alphabetic characters')

    class Meta:
        fields = ('id', 'state_name', 'cities')
        ordered = True


state_schema = StateSchema()
states_schema = StateSchema(many=True)
