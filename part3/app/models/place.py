from app import db
from app.models.base_model import BaseModel

# Many-to-Many üçün ara cədvəl
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # User ilə əlaqə (Foreign Key)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Review ilə əlaqə (Bir evin çoxlu rəyi ola bilər)
    # cascade="all, delete-orphan" -> Ev silinərsə, rəyləri də silinsin
    reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")

    # Amenity ilə əlaqə (Many-to-Many)
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places', lazy='subquery')
