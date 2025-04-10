import sqlite3
import os

db_path = os.path.join('db', 'gastrostock.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS marnotrawstwo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produkt TEXT,
    ilosc REAL,
    jednostka TEXT,
    powod TEXT,
    data TEXT DEFAULT CURRENT_DATE
)
""")

conn.commit()
conn.close()
print("✅ Tabela marnotrawstwo została utworzona.")
