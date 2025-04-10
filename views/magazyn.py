import streamlit as st
import sqlite3
import pandas as pd
import os

def show():
    st.header("📦 Magazyn")
    db_path = os.path.join('db', 'gastrostock.db')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM produkty", conn)
    conn.close()
    st.dataframe(df)
