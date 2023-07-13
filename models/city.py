from init import db, ma
from marshmallow import fields


class City(db.Model):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), nullable=False)

    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    state = db.relationship('State', back_populates='cities')
    addresses = db.relationship('Address', back_populates='city')


class CitySchema(ma.Schema):
    state = fields.Nested('StateSchema', exclude=('cities',))
    addresses = fields.Nested('AddressSchema', exclude=('city',), many=True)

    class Meta:
        fields = ('id', 'city_name', 'state')


city_schema = CitySchema()
cities_schema = CitySchema(many=True)
