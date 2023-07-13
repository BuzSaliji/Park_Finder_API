from init import db, ma
from marshmallow import fields


class Address(db.Model):
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(250), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    city = db.relationship('City', back_populates='addresses')


class AddressSchema(ma.Schema):
    city = fields.Nested('CitySchema', exclude=['cities'])

    class Meta:
        fields = ('id', 'address', 'city_id')
        ordered = True


address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)
