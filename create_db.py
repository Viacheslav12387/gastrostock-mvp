import sqlite3
import os

# 🔸 Ścieżka do pliku bazy danych
db_path = os.path.join('db', 'gastrostock.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 🔸 Tworzenie tabeli PRODUKTY
cursor.execute("""
CREATE TABLE IF NOT EXISTS produkty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produkt TEXT NOT NULL,
    jednostka TEXT,
    min_stan INTEGER,
    koszt REAL,
    dostawca TEXT,
    kategoria TEXT
);
""")

conn.commit()
conn.close()
print("✅ Baza danych i tabela zostały utworzone.")
