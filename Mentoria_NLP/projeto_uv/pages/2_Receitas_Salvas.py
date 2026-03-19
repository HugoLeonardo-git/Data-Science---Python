import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.mongo import get_database

st.set_page_config(
    page_title="Receitas Salvas",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Receitas Salvas")

db = get_database()
colecao = db["receitas"]

receitas = list(
    colecao.find({}, {
        "_id": 0,
        "nome_receita": 1,
        "tempo_preparo": 1,
        "rendimento": 1
    })
)

if receitas:
    df = pd.DataFrame(receitas)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nenhuma receita salva ainda.")