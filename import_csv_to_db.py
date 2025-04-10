import sqlite3
import pandas as pd
import os

# 🔹 Ścieżka do bazy
db_path = os.path.join('db', 'gastrostock.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 🔹 Wczytaj dane z CSV
df = pd.read_csv("produkty.csv")

# 🔁 Zmień nazwy kolumn na te zgodne z bazą danych
df = df.rename(columns={
    "Produkt": "produkt",
    "Jednostka": "jednostka",
    "Min. stan": "min_stan",
    "Koszt (zł)": "koszt",
    "Dostawca": "dostawca",
    "Kategoria": "kategoria"
})

# ✅ Wstaw dane do tabeli 'produkty'
for _, row in df.iterrows():
    # Pomiń, jeśli brak nazwy produktu
    if pd.isna(row["produkt"]) or row["produkt"] == "":
        continue

    cursor.execute("""
        INSERT INTO produkty (produkt, jednostka, min_stan, koszt, dostawca, kategoria)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        row["produkt"],
        row["jednostka"],
        int(row["min_stan"]) if not pd.isna(row["min_stan"]) else 0,
        float(row["koszt"]) if not pd.isna(row["koszt"]) else 0.0,
        row["dostawca"],
        row["kategoria"]
    ))



conn.commit()
conn.close()

print(f"✅ Zaimportowano {len(df)} produktów do bazy danych.")

