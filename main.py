from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.city_controller import city_bp
from controllers.state_controller import state_bp
from controllers.suburb_controller import suburb_bp
from controllers.address_controller import address_bp
from controllers.park_controller import park_bp
from controllers.review_controller import review_bp


def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(city_bp)
    app.register_blueprint(state_bp)
    app.register_blueprint(suburb_bp)
    app.register_blueprint(address_bp)
    app.register_blueprint(park_bp)
    app.register_blueprint(review_bp)

    return app
