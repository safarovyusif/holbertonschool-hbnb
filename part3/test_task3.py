import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"


def run_test():
    print("--- TASK 3 TESTİ BAŞLADI ---")

    # 1. Serverin işlədiyini yoxlayaq
    try:
        requests.get(f"{BASE_URL}/places/")
    except BaseException:
        print("❌ XƏTA: Server işləmir! Zəhmət olmasa 'python3 r \n   \n    \
    un.py' əmrini işə salın.")
        return

    # 2. Yeni İstifadəçi Yaradaq
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "owner@mail.com",
        "password": "123"
    }
    # Əgər köhnə varsa xəta verməsin deyə email dəyişə bilərsən və ya ignore et
    requests.post(f"{BASE_URL}/users/", json=user_data)
    print("✅ İstifadəçi yaradıldı (və ya artıq var).")

    # 3. Token Alaq (Login)
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "owner@mail.com", "password": "123"
    })

    if login_resp.status_code != 200:
        print(f"❌ XƏTA: Login uğursız oldu. Kod: {login_resp.status_code}")
        return

    token = login_resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Token alındı.")

    # 4. Ev Yaradaq
    place_data = {
        "title": "Sahibin Evi",
        "description": "Test",
        "price": 100,
        "latitude": 10,
        "longitude": 20
    }
    place_resp = requests.post(
        f"{BASE_URL}/places/",
        json=place_data,
        headers=headers)

    if place_resp.status_code != 201:
        print(f"❌ XƏTA: Ev yaradılmadı. Kod: {place_resp.status_code}")
        print("Cavab:", place_resp.text)
        return

    place_id = place_resp.json()['id']
    print(f"✅ Ev yaradıldı. ID: {place_id}")

    # 5. TESTİN ƏSAS HİSSƏSİ: Öz evinə rəy yazmağa cəhd et!
    print("⏳ Öz evinə rəy yazmağa cəhd edilir... (Xəta verməlidir)")

    review_data = {
        "place_id": place_id,
        "text": "Bu mənim öz evimdir!",
        "rating": 5
    }
    review_resp = requests.post(
        f"{BASE_URL}/reviews/",
        json=review_data,
        headers=headers)

    # Nəticəni yoxlayaq
    if review_resp.status_code == 400:
        print("🎉 TƏBRİKLƏR! Sistem icazə vermədi. Cavab:", review_resp.json())
        print("✅ TEST UĞURLUDUR!")
    else:
        print(f"❌ TEST UĞURSUZ OLDU. Kod: {review_resp.status_code}")
        print(
            "Sistem öz evinə rəy yazmağa icazə verdi (və ya ba \n   \n     \
    şqa xəta oldu).")


run_test()
