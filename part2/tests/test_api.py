import unittest
from app import create_app

class TestHBnB(unittest.TestCase):

    def setUp(self):
        """Hər testdən əvvəl işə düşür"""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        """User yaratmağı yoxlayır"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_create_user_invalid_email(self):
        """Səhv email validasiyasını yoxlayır"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "bad-email"  # @ işarəsi yoxdur
        })
        self.assertEqual(response.status_code, 400) # Xəta qayıtmalıdır

    def test_create_amenity(self):
        """Amenity yaratmağı yoxlayır"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Pool"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place(self):
        """Place yaratmağı yoxlayır (User və Amenity ilə birlikdə)"""
        # 1. User yarat
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Guy",
            "email": "owner@example.com"
        })
        user_id = user_res.json['id']

        # 2. Amenity yarat
        amenity_res = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        amenity_id = amenity_res.json['id']

        # 3. Place yarat
        place_res = self.client.post('/api/v1/places/', json={
            "title": "Test House",
            "description": "Testing",
            "price": 100.0,
            "latitude": 45.0,
            "longitude": 90.0,
            "owner_id": user_id,
            "amenities": [amenity_id]
        })
        self.assertEqual(place_res.status_code, 201)

    def test_create_place_negative_price(self):
        """Mənfi qiymət validasiyasını yoxlayır"""
        # User yaradaq (sahib lazımdır)
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Two",
            "email": "owner2@example.com"
        })
        user_id = user_res.json['id']

        response = self.client.post('/api/v1/places/', json={
            "title": "Bad Price House",
            "price": -50.0,  # Mənfi qiymət
            "latitude": 45.0,
            "longitude": 90.0,
            "owner_id": user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400) # Xəta qayıtmalıdır

if __name__ == '__main__':
    unittest.main()
