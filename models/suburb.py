from init import db, ma
from marshmallow import fields, validates, ValidationError


class Suburb(db.Model):
    __tablename__ = "suburb"

    id = db.Column(db.Integer, primary_key=True)
    suburb_name = db.Column(db.String(50), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    city = db.relationship('City', back_populates='suburbs')
    parks = db.relationship('Park', back_populates='suburb')


class SuburbSchema(ma.Schema):
    city = fields.Nested('CitySchema', exclude=['cities'])

    @validates('suburb_name')
    def validate_suburb_name(self, value):
        if not value.isalpha():
            raise ValidationError(
                'Suburb name should only contain alphabetic characters')

    class Meta:
        fields = ('id', 'suburb_name', 'city_id')
        ordered = True


suburb_schema = SuburbSchema()
suburbs_schema = SuburbSchema(many=True)
