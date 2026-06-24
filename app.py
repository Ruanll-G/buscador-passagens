import streamlit as st
import pandas as pd
import sqlite3

# =========================
# CARREGAR DADOS
# =========================

conn = sqlite3.connect("passagens.db")

def buscar(cidade):
    query = f"""
    SELECT *
    FROM passagens
    WHERE origem LIKE '%{cidade}%'
       OR destino LIKE '%{cidade}%'
       OR "origem(vlt)" LIKE '%{cidade}%'
       OR "destino(vlt)" LIKE '%{cidade}%'
    """
    return pd.read_sql(query, conn)

# =========================
# TÍTULO
# =========================

st.title("🔎 Buscador de Passagens")

# =========================
# FORMATAÇÃO DE COLUNAS
#==========================

def format_preco(x):
    try:
        x = float(x)
        return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return x

def format_data(col):
    return pd.to_datetime(col, errors="coerce").dt.strftime("%d/%m/%Y")

# =========================
# INPUT (FILTRO)
# =========================

cidade = st.text_input("Digite a cidade (origem ou destino)")

# =========================
# FILTRO
# =========================
if cidade:
    resultado = buscar(cidade)
    resultado["data"] = format_data(resultado["data"])
    resultado["preço"] = resultado["preço"].apply(format_preco)
    st.subheader("🟦 IDA")
    st.dataframe(
        resultado[["origem", "destino", "data", "preço"]]
    )

    st.subheader("🟧 VOLTA")
    resultado["data(vlt)"] = format_data(resultado["data(vlt)"])
    resultado["preço(vlt)"] = resultado["preço(vlt)"].apply(format_preco)
    st.dataframe(
        resultado[["origem(vlt)", "destino(vlt)", "data(vlt)", "preço(vlt)"]]
    )