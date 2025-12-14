from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = []
        self.place_repo = []
        self.review_repo = []
        self.amenity_repo = []

    # --- User Logic ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.append(user)
        return user

    def get_user(self, user_id):
        return next((u for u in self.user_repo if u.id == user_id), None)

    def get_user_by_email(self, email):
        return next((u for u in self.user_repo if u.email == email), None)

    # --- Place Logic ---
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.append(place)
        return place

    def get_place(self, place_id):
        return next((p for p in self.place_repo if p.id == place_id), None)

    def get_all_places(self):
        return self.place_repo

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if place:
            place.update(data)
        return place

    # --- Review Logic ---
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.append(review)
        return review

    def get_review(self, review_id):
        return next((r for r in self.review_repo if r.id == review_id), None)

    def get_all_reviews(self):
        return self.review_repo

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo if r.place_id == place_id]

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if review:
            review.update(data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if review:
            self.review_repo.remove(review)
            return True
        return False

    # --- Amenity Logic ---
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.append(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return next((a for a in self.amenity_repo if a.id == amenity_id), None)

    def get_all_amenities(self):
        return self.amenity_repo
