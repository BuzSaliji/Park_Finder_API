from init import db, ma
from marshmallow import fields


class State(db.Model):
    __tablename__ = 'state'

    id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(50), nullable=False)

    cities = db.relationship('City', back_populates='state')


class StateSchema(ma.Schema):
    cities = fields.Nested('CitySchema', many=True, exclude=['state'])

    class Meta:
        fields = ('id', 'state_name', 'cities')
        ordered = True


state_schema = StateSchema()
states_schema = StateSchema(many=True)
