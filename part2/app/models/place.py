from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # Relationship: Rəylər siyahısı
        self.amenities = []  # Relationship: Rahatlıqlar siyahısı

        # Validasiyalar
        if not title or len(title) > 100:
            raise ValueError("Title is required and must be max 100 chars")
        if price < 0:
            raise ValueError("Price must be a positive value")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")
        if not isinstance(owner, User):
            raise ValueError("Owner must be a valid User instance")

    def add_review(self, review):
        """Evi rəy siyahısına əlavə edir"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Evə rahatlıq (amenity) əlavə edir"""
        self.amenities.append(amenity)
