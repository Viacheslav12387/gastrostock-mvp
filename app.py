import streamlit as st
import sqlite3
import pandas as pd
import os
import pandas as pd


# 🔹 Połączenie z bazą
db_path = os.path.join('db', 'gastrostock.db')
conn = sqlite3.connect(db_path)

# 🔍 Wczytaj dane do DataFrame
df = pd.read_sql_query("SELECT * FROM produkty", conn)

st.title("📦 Magazyn Gastronomii")
st.subheader("Dane z bazy SQLite")

# 🔍 Filtrowanie
kategorie = df['kategoria'].dropna().unique().tolist()
dostawcy = df['dostawca'].dropna().unique().tolist()

kategoria_filter = st.selectbox("Wybierz kategorię", ["Wszystkie"] + kategorie)
dostawca_filter = st.selectbox("Wybierz dostawcę", ["Wszystkie"] + dostawcy)

filtered_df = df.copy()

if kategoria_filter != "Wszystkie":
    filtered_df = filtered_df[filtered_df['kategoria'] == kategoria_filter]

if dostawca_filter != "Wszystkie":
    filtered_df = filtered_df[filtered_df['dostawca'] == dostawca_filter]

# 🔴 Alerty niskiego stanu
st.markdown("### 🛑 Produkty o niskim stanie:")
low_stock = filtered_df[filtered_df['min_stan'] <= 2]
st.dataframe(low_stock)

# 📋 Główna tabela
st.markdown("### 📋 Wszystkie produkty:")
st.dataframe(filtered_df)

conn.close()

st.header("➕ Dodaj nowy produkt")

with st.form("add_product_form"):
    produkt = st.text_input("Nazwa produktu")
    jednostka = st.text_input("Jednostka (np. kg, szt)")
    min_stan = st.number_input("Minimalny stan", min_value=0)
    koszt = st.number_input("Koszt", min_value=0.0, step=0.01)
    dostawca = st.text_input("Dostawca")
    kategoria = st.text_input("Kategoria")

    submitted = st.form_submit_button("Dodaj produkt")

    if submitted:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produkty (produkt, jednostka, min_stan, koszt, dostawca, kategoria)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (produkt, jednostka, min_stan, koszt, dostawca, kategoria))
        conn.commit()
        conn.close()
        st.success("✅ Produkt dodany!")
        st.experimental_rerun()


st.header("📊 Statystyki magazynowe")

total_items = len(filtered_df)
total_value = (filtered_df["koszt"] * filtered_df["min_stan"]).sum()

st.markdown(f"**🔢 Liczba produktów:** {total_items}")
st.markdown(f"**💰 Wartość zapasu (netto):** {total_value:.2f} zł")

low_stock_crit = filtered_df[filtered_df['min_stan'] <= 2]
st.markdown("### ❗ Produkty poniżej minimalnego stanu")
st.dataframe(low_stock_crit)

st.markdown("### 🗑️ Usuń produkt")

product_ids = filtered_df["id"].tolist()
delete_id = st.selectbox("Wybierz ID produktu do usunięcia", [""] + [str(i) for i in product_ids])

if delete_id:
    if st.button("Usuń"):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produkty WHERE id = ?", (delete_id,))
        conn.commit()
        conn.close()
        st.success(f"✅ Produkt o ID {delete_id} został usunięty.")
        st.experimental_rerun()


st.markdown("### 🧾 Liczba produktów wg kategorii")
st.bar_chart(filtered_df["kategoria"].value_counts())

st.markdown("### 📤 Eksportuj dane do CSV")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Pobierz CSV", data=csv, file_name="produkty.csv", mime="text/csv")

st.header("♻️ Marnowanie jedzenia")

# Formularz marnowania
with st.form("waste_form"):
    waste_product = st.selectbox("Wybierz produkt", df["produkt"].unique())
    waste_amount = st.number_input("Ilość", min_value=0.1)
    waste_unit = st.selectbox("Jednostka", df["jednostka"].unique())
    waste_reason = st.text_input("Powód (np. przeterminowane, uszkodzone)")
    waste_submit = st.form_submit_button("Zapisz stratę")

    if waste_submit:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO marnotrawstwo (produkt, ilosc, jednostka, powod)
            VALUES (?, ?, ?, ?)
        """, (waste_product, waste_amount, waste_unit, waste_reason))
        conn.commit()
        conn.close()
        st.success("✅ Zapisano marnowanie!")
        st.experimental_rerun()



st.markdown("### 📉 Historia strat")

conn = sqlite3.connect(db_path)
waste_df = pd.read_sql_query("SELECT * FROM marnotrawstwo ORDER BY data DESC", conn)
conn.close()

st.dataframe(waste_df)

# Statystyka
total_waste = waste_df["ilosc"].sum()
st.markdown(f"**🔢 Łącznie zmarnowano:** {total_waste:.2f} jednostek")
