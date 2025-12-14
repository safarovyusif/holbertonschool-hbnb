import uuid
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Parolu hash'ləyirik
pw_hash = bcrypt.generate_password_hash("admin1234").decode('utf-8')

sql_content = f"""
INSERT INTO users (id, email, password, first_name, last_name, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    '{pw_hash}',
    'Admin',
    'HBnB',
    1
);

INSERT INTO amenities (id, name) VALUES 
    ('{str(uuid.uuid4())}', 'WiFi'),
    ('{str(uuid.uuid4())}', 'Swimming Pool'),
    ('{str(uuid.uuid4())}', 'Air Conditioning');
"""

with open("data.sql", "w") as f:
    f.write(sql_content)

print("data.sql generated successfully with valid password hash!")
