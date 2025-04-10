import sqlite3
import os

db_path = os.path.join('db', 'gastrostock.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("📦 Kategorie w bazie:")
cursor.execute("SELECT DISTINCT kategoria FROM produkty")
for row in cursor.fetchall():
    print("•", row[0])

print("\n📦 Dostawcy w bazie:")
cursor.execute("SELECT DISTINCT dostawca FROM produkty")
for row in cursor.fetchall():
    print("•", row[0])

conn.close()
