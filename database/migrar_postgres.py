import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# =========================
# SQLITE LOCAL
# =========================

sqlite_conn = sqlite3.connect("viagens.db")

# =========================
# POSTGRESQL SUPABASE
# =========================
password = quote_plus("J3@HWSx*d6dXQur")

DATABASE_URL = f"postgresql://postgres.lfayhozzilflwljuwsau:{password}@aws-1-sa-east-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DATABASE_URL)

# =========================
# LISTAR TABELAS SQLITE
# =========================

query = """
SELECT name
FROM sqlite_master
WHERE type='table'
"""

tabelas = pd.read_sql(query, sqlite_conn)

# =========================
# MIGRAR TABELAS
# =========================

for tabela in tabelas["name"]:

    print(f"Migrando tabela: {tabela}")

    df = pd.read_sql(
        f"SELECT * FROM {tabela}",
        sqlite_conn
    )

    df.to_sql(
        tabela,
        engine,
        if_exists="replace",
        index=False
    )

print("Migração concluída!")
