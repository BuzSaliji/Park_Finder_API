from init import db, ma
# from marshmallow import fields, validates, validationError

# Define address model


class Address(db.Model):
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    street_number = db.Column(db.String(20))
    street_name = db.Column(db.String(150), nullable=False)
    postcode = db.Column(db.String, nullable=False)
    suburb_id = db.Column(db.Integer, db.ForeignKey(
        'suburb.id'), nullable=False)

    suburb = db.relationship('Suburb', back_populates='addresses')

    park = db.relationship('Park', back_populates='address')


class AddressSchema(ma.Schema):

    class Meta:
        fields = ('id', 'street_number', 'street_name',
                  'postcode', 'suburb_id')

        ordered = True


address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)
