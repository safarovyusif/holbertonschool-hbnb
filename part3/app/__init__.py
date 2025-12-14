from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager  # <--- YENİ
from config import DevelopmentConfig

bcrypt = Bcrypt()
jwt = JWTManager()  # <--- YENİ

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)  # <--- YENİ

    from app.api.v1.users import users_bp
    from app.api.v1.places import places_bp
    from app.api.v1.reviews import reviews_bp
    from app.api.v1.amenities import amenities_bp
    from app.api.v1.auth import auth_bp  # <--- YENİ (Auth üçün blueprint)

    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(places_bp, url_prefix='/api/v1/places')
    app.register_blueprint(reviews_bp, url_prefix='/api/v1/reviews')
    app.register_blueprint(amenities_bp, url_prefix='/api/v1/amenities')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth') # <--- YENİ

    return app
