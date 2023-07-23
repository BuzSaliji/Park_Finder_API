from init import db, ma
from marshmallow import fields, validates, ValidationError


class Park(db.Model):
    __tablename__ = "park"

    id = db.Column(db.Integer, primary_key=True)
    park_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    suburb_id = db.Column(db.Integer, db.ForeignKey(
        'suburb.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    suburb = db.relationship('Suburb', back_populates='parks')
    user = db.relationship('User', back_populates='parks')
    reviews = db.relationship('Review', back_populates='park')


class ParkSchema(ma.Schema):
    suburb = fields.Nested('suburbSchema', exclude=['suburbs'])
    user = fields.Nested('UserSchema', exclude=['users'])

    @validates('park_name')
    def validate_park_name(self, value):
        if not value.isalpha():
            raise ValidationError(
                'Park name should only contain alphabetic characters')

    class Meta:
        fields = ('id', 'park_name',  'description',
                  'address', 'suburb_id', 'user_id')
        ordered = True


park_schema = ParkSchema()
parks_schema = ParkSchema(many=True)
