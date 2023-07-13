from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.city_controller import city_bp
from controllers.state_controller import state_bp


def create_app():
    app = Flask(__name__)

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

    return app
