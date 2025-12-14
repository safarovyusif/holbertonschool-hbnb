from app import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # User ilə əlaqə (Müəllif kimdir?)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Place ilə əlaqə (Hansı evə yazılıb?)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
