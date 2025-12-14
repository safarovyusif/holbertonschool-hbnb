import sqlite3

db_path = "instance/development.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Schema tətbiq edilir...")
with open("schema.sql", "r") as f:
    cursor.executescript(f.read())

print("Data əlavə edilir...")
with open("data.sql", "r") as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()
print("Bitdi! Bazanı yoxlaya bilərsən.")
