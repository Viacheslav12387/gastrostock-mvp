import streamlit as st
import sqlite3
import pandas as pd
import os

def show():
    st.header("♻️ Marnowanie jedzenia")
    db_path = os.path.join('db', 'gastrostock.db')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM produkty", conn)

    # FORMULARZ DODAWANIA STRATY
    with st.expander("➕ Dodaj nową stratę"):
        with st.form("waste_form"):
            produkt = st.selectbox("Produkt", df["produkt"].unique())
            jednostka = df[df["produkt"] == produkt]["jednostka"].values[0]
            ilosc = st.number_input(f"Ilość [{jednostka}]", min_value=0.1)
            powod = st.text_input("Powód (np. przeterminowane)")
            submit = st.form_submit_button("Zapisz stratę")

            if submit:
                conn.execute("""
                    INSERT INTO marnotrawstwo (produkt, ilosc, jednostka, powod)
                    VALUES (?, ?, ?, ?)
                """, (produkt, ilosc, jednostka, powod))
                conn.commit()
                st.success("✅ Zapisano stratę!")
                st.experimental_rerun()

    # HISTORIA STRAT
    st.markdown("### 📋 Historia strat")
    waste_df = pd.read_sql_query("SELECT * FROM marnotrawstwo ORDER BY data DESC", conn)

    if not waste_df.empty:
        for i, row in waste_df.iterrows():
            with st.expander(f"{row['data']} – {row['produkt']} ({row['ilosc']} {row['jednostka']})"):
                # Formularz edycji
                with st.form(f"edit_form_{row['id']}"):
                    new_produkt = st.selectbox("Produkt", df["produkt"].unique(), index=df["produkt"].tolist().index(row["produkt"]))
                    new_jednostka = df[df["produkt"] == new_produkt]["jednostka"].values[0]
                    new_ilosc = st.number_input("Ilość", value=row["ilosc"], key=f"ilosc_{row['id']}")
                    new_powod = st.text_input("Powód", value=row["powod"], key=f"powod_{row['id']}")
                    save_btn = st.form_submit_button("💾 Zapisz zmiany")

                    if save_btn:
                        conn.execute("""
                            UPDATE marnotrawstwo
                            SET produkt = ?, ilosc = ?, jednostka = ?, powod = ?
                            WHERE id = ?
                        """, (new_produkt, new_ilosc, new_jednostka, new_powod, row["id"]))
                        conn.commit()
                        st.success("✅ Zmiany zapisane!")
                        st.experimental_rerun()

                # Przycisk usuwania
                if st.button("🗑 Usuń", key=f"delete_{row['id']}"):
                    conn.execute("DELETE FROM marnotrawstwo WHERE id = ?", (row["id"],))
                    conn.commit()
                    st.warning("❌ Wpis usunięty")
                    st.rerun()
    else:
        st.info("Brak zapisanych strat.")

    conn.close()

