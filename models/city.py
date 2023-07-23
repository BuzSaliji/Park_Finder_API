from init import db, ma
from marshmallow import fields, validates, ValidationError


class City(db.Model):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), nullable=False)

    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    state = db.relationship('State', back_populates='cities')
    suburbs = db.relationship('Suburb', back_populates='city')


class CitySchema(ma.Schema):
    state = fields.Nested('StateSchema', exclude=['cities'])
    suburbs = fields.Nested('SuburbSchema', exclude=['city'], many=True)

    @validates('city_name')
    def validate_city_name(self, value):
        if not value.isalpha():
            raise ValidationError(
                'city name should only contain alphabetic characters')

    class Meta:
        fields = ('id', 'city_name', 'state')
        ordered = True


city_schema = CitySchema()
cities_schema = CitySchema(many=True)
