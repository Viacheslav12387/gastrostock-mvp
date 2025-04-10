import sqlite3
import os

# 🔹 Ścieżka do bazy danych
db_path = os.path.join('db', 'gastrostock.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 🔹 Pobierz wszystkie dane
cursor.execute("SELECT * FROM produkty")
produkty = cursor.fetchall()

# 🔹 Wyświetl dane
print("\n📋 Lista produktów w bazie danych:\n")
for produkt in produkty:
    print(f"ID: {produkt[0]} | Nazwa: {produkt[1]} | Jednostka: {produkt[2]} | Min. stan: {produkt[3]} | Koszt: {produkt[4]} zł | Dostawca: {produkt[5]} | Kategoria: {produkt[6]}")

conn.close()
