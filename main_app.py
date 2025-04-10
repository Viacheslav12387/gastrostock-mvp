import streamlit as st
from views import magazyn, straty, statystyki, eksport

st.sidebar.title("📂 Nawigacja")
page = st.sidebar.radio("Przejdź do:", ["Magazyn", "Straty", "Statystyki", "Eksport danych"])

if page == "Magazyn":
    magazyn.show()
elif page == "Straty":
    straty.show()
elif page == "Statystyki":
    statystyki.show()
elif page == "Eksport danych":
    eksport.show()
