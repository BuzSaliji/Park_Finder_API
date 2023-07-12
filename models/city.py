from init import db, ma


class City(db.Model):
    __tablename__ = "city"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.column(db.String(50), nullable=False)


class CitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'city_name')


city_schema = CitySchema()
cities_schema = CitySchema(many=True)
