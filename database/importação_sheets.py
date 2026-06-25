
import pandas as pd
import sqlite3

# =========================
# CONFIGURAÇÃO
# =========================

SHEET_ID = "1ORQs9PZpsBtiacclthsETMuz1hm-brG-8j1N2Snmx7w"

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx"

# =========================
# CONEXÃO SQLITE
# =========================

conn = sqlite3.connect("viagens.db")

# =========================
# LER TODAS AS ABAS
# =========================

sheets = pd.read_excel(
    url,
    sheet_name=None
)

# =========================
# MAPEAMENTO DE NOMES
# =========================

nomes_tabelas = {
    "Inicio": "inicio",
    "Inicio + 7 dias": "inicio_7_dias",
    "Inicio + 30 dias": "inicio_30_dias"
}

# =========================
# IMPORTAÇÃO
# =========================

for nome_aba, df in sheets.items():

    # limpar nomes das colunas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # pegar nome da tabela
    tabela = nomes_tabelas.get(nome_aba)

    if tabela:

        # salvar no sqlite
        df.to_sql(
            tabela,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"Tabela '{tabela}' criada com sucesso!")

# =========================
# FECHAR CONEXÃO
# =========================

conn.close()

print("Importação concluída!")

