from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.state import State
from models.city import City
from models.suburb import Suburb
from models.address import Address
from models.park import Park
from models.review import Review

db_commands = Blueprint('db', __name__)


@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")


@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            username='admin',
            email='admin@admin.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        User(
            username='User1',
            email='user1@email.com',
            password=bcrypt.generate_password_hash('user1pw').decode('utf-8')
        )
    ]

    db.session.add_all(users)

    # Seed states


@db_commands.cli.command('seed')
def seed_db():
    # Seed users
    users = [
        User(
            username='admin',
            email='admin@admin.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        ),
        User(
            username='User1',
            email='user1@email.com',
            password=bcrypt.generate_password_hash('user1pw').decode('utf-8')
        )
    ]
    db.session.add_all(users)
    db.session.commit()

    # Seed states
    states = [
        State(state_name='New South Wales'),
        State(state_name='Victoria'),
        State(state_name='Queensland'),
        State(state_name='Western Australia'),
        State(state_name='South Australia'),
        State(state_name='ACT'),
        State(state_name='Tasmania'),
    ]
    db.session.add_all(states)
    db.session.commit()

    # Seed cities
    city = [
        ('Sydney', 'New South Wales'),
        ('Melbourne', 'Victoria'),
        ('Brisbane', 'Queensland'),
        ('Perth', 'Western Australia'),
        ('Adelaide', 'South Australia'),
        ('Canberra', 'ACT'),
        ('Hobart', 'Tasmania'),
        ('Wollongong', 'New South Wales'),
    ]
    for city_name, state_name in city:
        stmt = db.select(State.id).where(State.state_name == state_name)
        state_id = db.session.execute(stmt).scalar()
        db.session.add(City(city_name=city_name, state_id=state_id))
    db.session.commit()

    # Seed suburbs
    suburb = [
        ('Newington', 'Sydney'),
        ('Wallan', 'Melbourne'),
        ('Seventeen Mile Rocks', 'Brisbane'),
        ('Whiteman', 'Perth'),
        ('St Kilda', 'Adelaide'),
        ('Molonglo Valley', 'Canberra'),
        ('Battery Point', 'Hobart'),
        ('Fairy Meadow', 'Wollongong'),
    ]
    for suburb_name, city_name in suburb:
        stmt = db.select(City.id).where(City.city_name == city_name)
        city_id = db.session.execute(stmt).scalar()
        db.session.add(Suburb(suburb_name=suburb_name, city_id=city_id))
    db.session.commit()

    # Seed addresses
    addresses = [
        (147, 'Jamieson St', 2127, 'Newington'),
        (1251, 'Melbourne Rd', 3756, 'Wallan'),
        (5, 'Counihan Rd', 4073, 'Seventeen Mile Rocks'),
        (147, 'Lord St & W Swan Rd', 6068, 'Whiteman'),
        (5, '5th St', 3182, 'St Kilda'),
        (34, 'Forest Dr', 2611, 'Molonglo Valley'),
        (112, 'Salamanca Pl', 7004, 'Battery Point'),
        (99, 'Ellen St', 2500, 'Fairy Meadow'),
    ]
    for street_number, street_name, postcode, suburb_name in addresses:
        stmt = db.select(Suburb.id).where(Suburb.suburb_name == suburb_name)
        suburb_id = db.session.execute(stmt).scalar()
        db.session.add(Address(street_number=street_number, street_name=street_name,
                               postcode=postcode, suburb_id=suburb_id))
    db.session.commit()

    # Seed parks
    parks = [
        ('Blaxland Riverside Park', 'Blaxland Riverside Park is a sprawling park located in the suburb of Newington, Sydney. It offers a wide range of activities for children, including climbing ropes, giant slides, swings, a flying fox, and sand play areas. The park also features bike tracks, water play areas, and plenty of open space for picnics and ball games.', 'Jamieson St', 147, 2127, 'admin'),

        ('Adventure Park', 'Adventure Park is a popular theme park located in Wallan, just outside of Melbourne. It offers a variety of attractions and rides suitable for kids of all ages, including water slides, pools, mini-golf, paddle boats, and a dedicated play area with climbing structures and a maze. Its a great place for a day of thrilling adventures and family fun.', 'Melbourne Rd', 1251, 3756, 'admin'),

        ('Rocks Riverside Park', 'Rocks Riverside Park is a spacious park situated in the suburb of Seventeen Mile Rocks, Brisbane. It features an extensive playground with climbing nets, slides, swings, and a large sand play area. The park also offers bike tracks, basketball courts, a flying fox, and riverside picnic spots, making it an ideal destination for outdoor activities and family gatherings.', 'Counihan Rd', 5, 4073, 'admin'),

        ('Whiteman Park', 'Whiteman Park is a large recreational area located in the suburb of Whiteman, near Perth. It offers several childrens playgrounds with various play equipment, including slides, swings, and climbing structures. The park also features a tram ride, mini train, wildlife encounters, walking trails, and open spaces for picnics and nature exploration.', 'Lord St & W Swan Rd', 147, 6068, 'admin'),

        ('St Kilda Adventure Playground', 'St Kilda Adventure Playground is a popular destination for kids located in the suburb of St Kilda, Adelaide. The park offers a range of unique play structures, including pirate ships, slides, treehouses, and flying foxes. It also features a water play area, BMX track, mini-golf, and plenty of shady spots for picnics and relaxation.', '5th St', 5, 3182, 'admin'),

        ('Pod Playground at the National Arboretum', 'The Pod Playground is a creative and nature-themed play space located within the National Arboretum in the Molonglo Valley, Canberra. The park features giant acorn-shaped climbing frames, slides, and swings. Kids can also explore the nearby forests and enjoy the beautiful views of the city. The Pod Playground offers a unique blend of play and nature appreciation.', 'Forest Dr', 34, 2611, 'admin'),

        ('Battery Point Sculpture Trail', 'A walkable trail with various sculptures located in the historic suburb of Battery Point, Hobart. It offers a unique blend of art and history.', 'Salamanca Pl', 112, 7004, 'admin'),

        ('Fairy Meadow Beach Park', 'A beautiful beach park located in the suburb of Fairy Meadow, Wollongong. It offers a great place for a family picnic with playgrounds, BBQ areas, and clean sandy beach.', 'Ellen St', 99, 2500, 'admin'),
    ]
    for park_name, description, street_name, street_number, postcode, username in parks:
        stmt_address = db.select(Address.id).where(
            (Address.street_name == street_name) &
            (Address.street_number == street_number) &
            (Address.postcode == postcode)
        )
        address_id = db.session.execute(stmt_address).scalar()

        stmt_user = db.select(User.id).where(User.username == username)
        user_id = db.session.execute(stmt_user).scalar()

        db.session.add(Park(park_name=park_name, description=description,
                            address_id=address_id, user_id=user_id))
    db.session.commit()

    # Seed reviews
    reviews_data = [
        (1, 1, 6, 'Nice park'),
        (1, 2, 6, 'Nice park'),
        (1, 3, 9, 'Wonderful sculpture trail in a beautiful suburb.'),
        (1, 8, 10, 'Amazing beach park with a lot of amenities. A must visit in Wollongong.'),
    ]
    for user_id, park_id, rating, comment in reviews_data:
        db.session.add(Review(user_id=user_id, park_id=park_id,
                              rating=rating, comment=comment))
    db.session.commit()

    print("Tables Seeded")
