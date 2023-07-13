from init import db, ma
from marshmallow import fields


class City(db.Model):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), nullable=False)

    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    state = db.relationship('State', back_populates='cities')


class CitySchema(ma.Schema):
    state = fields.Nested('StateSchema', exclude=('cities',))

    class Meta:
        fields = ('id', 'city_name', 'state_id')


city_schema = CitySchema()
cities_schema = CitySchema(many=True)
