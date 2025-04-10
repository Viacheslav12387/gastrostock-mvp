import sqlite3
import os

# 🔹 Połączenie z bazą
db_path = os.path.join('db', 'gastrostock.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔍 Co chcesz przefiltrować?")
print("1 – Kategoria")
print("2 – Dostawca")

choice = input("Wybierz 1 lub 2: ")

if choice == "1":
    category = input("Wpisz nazwę kategorii (np. Nabiał, Warzywa, Półprodukty): ")
    cursor.execute("""
        SELECT produkt, jednostka, min_stan, koszt, dostawca, kategoria
        FROM produkty
        WHERE kategoria = ?
    """, (category,))
elif choice == "2":
    supplier = input("Wpisz nazwę dostawcy (np. Cheff, Lidl, Warzywniak): ")
    cursor.execute("""
        SELECT produkt, jednostka, min_stan, koszt, dostawca, kategoria
        FROM produkty
        WHERE dostawca = ?
    """, (supplier,))
else:
    print("❌ Niepoprawny wybór!")
    conn.close()
    exit()

produkty = cursor.fetchall()

print("\n📋 Wyniki filtrowania:\n")
for p in produkty:
    print(f"• {p[0]} ({p[1]}) | Min: {p[2]} | Koszt: {p[3]} zł | {p[4]} | {p[5]}")

conn.close()
