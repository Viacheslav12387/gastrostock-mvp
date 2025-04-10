import streamlit as st
import sqlite3
import pandas as pd
import os

def show():
    st.header("📊 Statystyki")

    db_path = os.path.join('db', 'gastrostock.db')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM produkty", conn)
    conn.close()

    total_items = len(df)
    total_value = (df["koszt"] * df["min_stan"]).sum()

    st.metric("🔢 Liczba produktów", total_items)
    st.metric("💰 Wartość zapasu (netto)", f"{total_value:.2f} zł")
    st.bar_chart(df["kategoria"].value_counts())
