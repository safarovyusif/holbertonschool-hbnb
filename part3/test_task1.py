from app.models.user import User

print("--- TEST BAŞLADI ---")

# 1. Yeni istifadəçi yaradırıq (parol: 'gizli123')
try:
    user = User(first_name="Ali", last_name="Aliyev", email="ali@mail.com", password="gizli123")
    print("✅ User obyekti yaradıldı.")
except Exception as e:
    print(f"❌ XƏTA: User yaradılarkən problem oldu: {e}")
    exit()

# 2. Parolun şifrələndiyini yoxlayırıq
# Şifrələnmiş parol $2b$ ilə başlamalıdır və 'gizli123' olmamalıdır
if user.password != "gizli123" and user.password.startswith("$2b$"):
    print(f"✅ UĞURLU: Parol şifrələnib (Hash): {user.password}")
else:
    print(f"❌ XƏTA: Parol açıq şəkildə qalıb və ya şifrələnməyib: {user.password}")

# 3. verify_password funksiyasını yoxlayırıq
if user.verify_password("gizli123"):
    print("✅ UĞURLU: verify_password düzgün parolu tanıdı.")
else:
    print("❌ XƏTA: verify_password düzgün parolu tanımadı.")

if not user.verify_password("sehvparol"):
    print("✅ UĞURLU: verify_password səhv parolu rədd etdi.")
else:
    print("❌ XƏTA: verify_password səhv parolu qəbul etdi!")

print("--- TEST BİTDİ ---")
