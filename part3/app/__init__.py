from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Namespaces import
    from app.api.v1.users import users_bp
    from app.api.v1.places import places_bp
    from app.api.v1.reviews import reviews_bp
    from app.api.v1.auth import auth_bp
    from app.api.v1.amenities import amenities_bp

    # Register blueprints
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(places_bp, url_prefix='/api/v1/places')
    app.register_blueprint(reviews_bp, url_prefix='/api/v1/reviews')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(amenities_bp, url_prefix='/api/v1/amenities')

    return app
