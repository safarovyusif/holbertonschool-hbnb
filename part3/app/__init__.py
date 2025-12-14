from flask import Flask
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig

bcrypt = Bcrypt()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)

    from app.api.v1.users import users_bp
    from app.api.v1.places import places_bp
    from app.api.v1.reviews import reviews_bp
    from app.api.v1.amenities import amenities_bp

    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(places_bp, url_prefix='/api/v1/places')
    app.register_blueprint(reviews_bp, url_prefix='/api/v1/reviews')
    app.register_blueprint(amenities_bp, url_prefix='/api/v1/amenities')

    return app
