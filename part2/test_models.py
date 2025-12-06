from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

try:
    # 1. User yaradaq
    user = User(first_name="Ali", last_name="Valiyev", email="ali@example.com")
    print(f"✅ User yaradıldı: {user.first_name} (ID: {user.id})")

    # 2. Place yaradaq
    place = Place(title="Dəniz kənarı villa", description="Gözəl mənzərə", price=150.0, 
                  latitude=40.4093, longitude=49.8671, owner=user)
    print(f"✅ Place yaradıldı: {place.title} - Sahibi: {place.owner.first_name}")

    # 3. Amenity yaradaq və əlavə edək
    wifi = Amenity(name="WiFi")
    place.add_amenity(wifi)
    print(f"✅ Amenity əlavə edildi: {place.amenities[0].name}")

    # 4. Review yaradaq və əlavə edək
    review = Review(text="Çox gözəl yerdir!", rating=5, place=place, user=user)
    place.add_review(review)
    print(f"✅ Review əlavə edildi: {place.reviews[0].text} - Reytinq: {place.reviews[0].rating}")

except Exception as e:
    print(f"❌ XƏTA: {e}")
