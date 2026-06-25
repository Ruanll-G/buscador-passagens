import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# =========================
# CARREGAR DADOS
# =========================

DATABASE_URL = st.secrets["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

# =========================
# TÍTULO
# =========================

st.title("🔎 Buscador de Passagens")
st.header("Inicio da pesquisa: 23/06/2026")

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

periodo = st.selectbox(
    "📅 Período",
    [
        "inicio",
        "inicio_7_dias",
        "inicio_30_dias"
    ]
)

origens_query = f"""
SELECT DISTINCT origem
FROM {periodo}
WHERE origem IS NOT NULL
ORDER BY origem
"""

destinos_query = f"""
SELECT DISTINCT destino
FROM {periodo}
WHERE destino IS NOT NULL
ORDER BY destino
"""

cidades_origem = pd.read_sql(origens_query, engine)["origem"].tolist()
cidades_destino = pd.read_sql(destinos_query, engine)["destino"].tolist()

# =========================
# FILTRO
# =========================
col1, col2 = st.columns(2)

with col1:
    origem = st.selectbox(
         "🛫 Origem",
         cidades_origem
    )

with col2:
    destino = st.selectbox(
         "🛬 Destino",
         cidades_destino
    )

query = f"""
SELECT *
FROM {periodo}
WHERE origem = %s
AND destino = %s
"""

#RESULTADO

resultado = pd.read_sql(
    query,
    engine,
    params=(origem, destino)
)


if not resultado.empty:

    resultado["data"] = format_data(resultado["data"])
    resultado["preço"] = resultado["preço"].apply(format_preco)

    resultado["data(vlt)"] = format_data(resultado["data(vlt)"])
    resultado["preço(vlt)"] = resultado["preço(vlt)"].apply(format_preco)

    # =========================
    # IDA
    # =========================

    st.subheader("🟦 IDA")

    st.dataframe(
        resultado[
            ["origem", "destino", "data", "preço"]
        ],
        use_container_width=True
    )

    # =========================
    # VOLTA
    # =========================

    st.subheader("🟧 VOLTA")

    st.dataframe(
        resultado[
            ["origem(vlt)", "destino(vlt)", "data(vlt)", "preço(vlt)"]
        ],
        use_container_width=True
    )

else:
    st.warning("Nenhuma passagem encontrada.")



