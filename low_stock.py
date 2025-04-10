import sqlite3
import os

# 🔹 Ścieżka do bazy
db_path = os.path.join('db', 'gastrostock.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 🔎 Wybieramy tylko produkty poniżej minimalnego stanu
cursor.execute("""
    SELECT produkt, jednostka, min_stan, koszt, dostawca, kategoria
    FROM produkty
    WHERE min_stan > 0 AND koszt < 999
""")

produkty = cursor.fetchall()

print("\n🛑 Produkty wymagające uzupełnienia:\n")
for p in produkty:
    print(f"• {p[0]} ({p[1]}) | Min: {p[2]} | Koszt: {p[3]} zł | {p[4]} | {p[5]}")

conn.close()