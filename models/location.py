from init import db, ma
from marshmallow import fields


class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    Address = db.Column(db.String(250), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city_id'), nullable=False)

    city = db.relationship('city', back_populates='location')

    class LocationSchema(ma.Schema):
        city = fields.Nested('citySchema', exclude=('cities',))

        class Meta:
            fields = ('id', 'address', 'city_id')

    location_schema = LocationSchema()
    locations_schema = LocationSchema(many=True)
