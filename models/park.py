from init import db, ma
from marshmallow import fields


class Park(db.Model):
    __tablename__ = "park"

    id = db.Column(db.Integer, primary_key=True)
    park_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey(
        'address.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    address = db.relationship('Address', back_populates='parks')
    user = db.relationship('User', back_populates='users')


class ParkSchema(ma.Schema):
    address = fields.Nested('AddressSchema', exclude=('addresses',))
    user = fields.Nested('UserSchema', exclude=('users',))

    class Meta:
        fields = ('id', 'park_name', 'description', 'address_id', 'user_id')


park_schema = ParkSchema()
parks_schema = ParkSchema(many=True)
