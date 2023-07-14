from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.state import State
from models.city import City
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
    states = [
        State(state_name='New South Wales'),
        State(state_name='Victoria'),
        State(state_name='Queensland'),
        State(state_name='Western Australia'),
        State(state_name='South Australia'),
        State(state_name='ACT'),
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
    ]

    db.session.add_all(cities)
    db.session.commit()

    print("Tables Seeded")
