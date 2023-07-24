from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.state import State
from models.city import City
from models.suburb import Suburb
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
    db.session.commit()  # Commit so that we have the IDs for the next step

    # Seed cities
    cities = [
        City(city_name='Sydney', state_id=State.query.filter_by(
            state_name='New South Wales').first().id),
        City(city_name='Melbourne', state_id=State.query.filter_by(
            state_name='Victoria').first().id),
        City(city_name='Brisbane', state_id=State.query.filter_by(
            state_name='Queensland').first().id),
        City(city_name='Perth', state_id=State.query.filter_by(
            state_name='Western Australia').first().id),
        City(city_name='Adelaide', state_id=State.query.filter_by(
            state_name='South Australia').first().id),
        City(city_name='Canberra', state_id=State.query.filter_by(
            state_name='ACT').first().id),
        City(city_name='Hobart', state_id=State.query.filter_by(
            state_name='Tasmania').first().id),
        City(city_name='Wollongong', state_id=State.query.filter_by(
            state_name='New South Wales').first().id),
    ]

    db.session.add_all(cities)
    db.session.commit()

    # Seed suburbs
    suburbs = [
        Suburb(suburb_name='Newington', city_id=City.query.filter_by(
            city_name='Sydney').first().id),
        Suburb(suburb_name='Wallan', city_id=City.query.filter_by(
            city_name='Melbourne').first().id),
        Suburb(suburb_name='Seventeen Mile Rocks',
               city_id=City.query.filter_by(city_name='Brisbane').first().id),
        Suburb(suburb_name='Whiteman', city_id=City.query.filter_by(
            city_name='Perth').first().id),
        Suburb(suburb_name='St Kilda', city_id=City.query.filter_by(
            city_name='Adelaide').first().id),
        Suburb(suburb_name='Molonglo Valley', city_id=City.query.filter_by(
            city_name='Canberra').first().id),
        Suburb(suburb_name='Battery Point', city_id=City.query.filter_by(
            city_name='Hobart').first().id),
        Suburb(suburb_name='Fairy Meadow', city_id=City.query.filter_by(
            city_name='Wollongong').first().id),
    ]

    db.session.add_all(suburbs)
    db.session.commit()

    parks = [
        Park(park_name='Blaxland Riverside Park', description='Blaxland Riverside Park is a sprawling park located in the suburb of Newington, Sydney. It offers a wide range of activities for children, including climbing ropes, giant slides, swings, a flying fox, and sand play areas. The park also features bike tracks, water play areas, and plenty of open space for picnics and ball games.', address='Jamieson St', suburb_id=Suburb.query.filter_by(
            suburb_name='Newington').first().id, user_id=User.query.filter_by(username='admin').first().id),
        Park(park_name='Adventure Park', description='Adventure Park is a popular theme park located in Wallan, just outside of Melbourne. It offers a variety of attractions and rides suitable for kids of all ages, including water slides, pools, mini-golf, paddle boats, and a dedicated play area with climbing structures and a maze. Its a great place for a day of thrilling adventures and family fun.', address='1251 Melbourne Rd', suburb_id=Suburb.query.filter_by(
            suburb_name='Wallan').first().id, user_id=User.query.filter_by(username='admin').first().id),
        Park(park_name='Rocks Riverside Park', description='Rocks Riverside Park is a spacious park situated in the suburb of Seventeen Mile Rocks, Brisbane. It features an extensive playground with climbing nets, slides, swings, and a large sand play area. The park also offers bike tracks, basketball courts, a flying fox, and riverside picnic spots, making it an ideal destination for outdoor activities and family gatherings.', address=' 5 Counihan Rd', suburb_id=Suburb.query.filter_by(
            suburb_name='Seventeen Mile Rocks').first().id, user_id=User.query.filter_by(username='admin').first().id),
        Park(park_name='Whiteman Park', description='Whiteman Park is a large recreational area located in the suburb of Whiteman, near Perth. It offers several childrens playgrounds with various play equipment, including slides, swings, and climbing structures. The park also features a tram ride, mini train, wildlife encounters, walking trails, and open spaces for picnics and nature exploration.', address='Lord St & W Swan Rd', suburb_id=Suburb.query.filter_by(
            suburb_name='Whiteman').first().id, user_id=User.query.filter_by(username='admin').first().id),
        Park(park_name='St Kilda Adventure Playground', description='St Kilda Adventure Playground is a popular destination for kids located in the suburb of St Kilda, Adelaide. The park offers a range of unique play structures, including pirate ships, slides, treehouses, and flying foxes. It also features a water play area, BMX track, mini-golf, and plenty of shady spots for picnics and relaxation.', address='5th St', suburb_id=Suburb.query.filter_by(
            suburb_name='St Kilda').first().id, user_id=User.query.filter_by(username='admin').first().id),
        Park(park_name='Pod Playground at the National Arboretum', description='The Pod Playground is a creative and nature-themed play space located within the National Arboretum in the Molonglo Valley, Canberra. The park features giant acorn-shaped climbing frames, slides, and swings. Kids can also explore the nearby forests and enjoy the beautiful views of the city. The Pod Playground offers a unique blend of play and nature appreciation.', address='Forest Dr', suburb_id=Suburb.query.filter_by(
            suburb_name='Molonglo Valley').first().id, user_id=User.query.filter_by(username='admin').first().id),
        Park(park_name='Battery Point Sculpture Trail', description='A walkable trail with various sculptures located in the historic suburb of Battery Point, Hobart. It offers a unique blend of art and history.',
             address='Salamanca Pl', suburb_id=Suburb.query.filter_by(suburb_name='Battery Point').first().id, user_id=User.query.filter_by(username='admin').first().id),
        Park(park_name='Fairy Meadow Beach Park', description='A beautiful beach park located in the suburb of Fairy Meadow, Wollongong. It offers a great place for a family picnic with playgrounds, BBQ areas, and clean sandy beach.', address='Ellen St', suburb_id=Suburb.query.filter_by(
            suburb_name='Fairy Meadow').first().id, user_id=User.query.filter_by(username='admin').first().id),
    ]

    db.session.add_all(parks)
    db.session.commit()

    reviews = [
        Review(user_id=1, park_id=1, rating=6, comment='Nice park'),
        Review(user_id=1, park_id=2, rating=6, comment='Nice park'),
        Review(user_id=1, park_id=3, rating=9,
               comment='Wonderful sculpture trail in a beautiful suburb.'),
        Review(user_id=1, park_id=8, rating=10,
               comment='Amazing beach park with a lot of amenities. A must visit in Wollongong.'),
    ]

    db.session.add_all(reviews)
    db.session.commit()


print("Tables Seeded")
