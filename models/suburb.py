from init import db, ma
from marshmallow import fields


class Suburb(db.Model):
    __tablename__ = "suburb"

    id = db.Column(db.Integer, primary_key=True)
    suburb_name = db.Column(db.String(50), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    city = db.relationship('City', back_populates='suburbs')
    parks = db.relationship('Park', back_populates='suburb')


class SuburbSchema(ma.Schema):
    city = fields.Nested('CitySchema', exclude=['cities'])

    class Meta:
        fields = ('id', 'suburb', 'city_id')
        ordered = True


suburb_schema = SuburbSchema()
suburbs_schema = SuburbSchema(many=True)
