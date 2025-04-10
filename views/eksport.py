import streamlit as st
import sqlite3
import pandas as pd
import os

def show():
    st.header("📤 Eksport danych")

    db_path = os.path.join('db', 'gastrostock.db')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM marnotrawstwo", conn)
    conn.close()

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Pobierz CSV ze stratami", data=csv, file_name="straty.csv", mime="text/csv")
