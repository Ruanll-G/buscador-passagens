from google.oauth2.service_account import Credentials
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv
import gspread
import pandas as pd

load_dotenv()

#Banco de dados

DATABASE_URL = st.secrets["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

def get_sheet():
    
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
    ]
        
    creds_info = {
        "type": st.secrets["GOOGLE_CREDS_TYPE"],
        "project_id": st.secrets["GOOGLE_CREDS_ID"],
        "private_key_id": st.secrets["GOOGLE_PRIVATE_KEY_ID"],
        "private_key": st.secrets["GOOGLE_PRIVATE_KEY"],
        "client_email": st.secrets["GOOGLE_CLIENT_EMAIL"],
        "client_id": st.secrets["GOOGLE_CLIENT_ID"],
        "auth_uri": st.secrets["GOOGLE_AUTH_URI"],
        "token_uri": st.secrets["GOOGLE_TOKEN_URI"],
        "auth_provider_x509_cert_url": st.secrets["GOOGLE_AUTH_PROVIDER"],
        "client_x509_cert_url": st.secrets["GOOGLE_CLIENT_CERT"],
        "universe_domain": st.secrets["GOOGLE_DOMAIN"]
    }

    creds = Credentials.from_service_account_info(
        creds_info,
        scopes=scopes
    )

    client = gspread.authorize(creds)

    sheet = client.open("Pesquisa Preços | 23/06/2026")
    return sheet

def sync_all():
    sheet = get_sheet()

    abas = {
    "inicio": "inicio",
    "inicio_7_dias": "inicio + 7 dias",
    "inicio_30_dias": "inicio + 30 dias"
    }

    for tabela, aba in abas.items():
        data = sheet.worksheet(aba).get_all_records()
        df = pd.DataFrame(data)

        df.to_sql(
            tabela,
            engine,
            if_exists="replace",
            index=False
        )
    return {"status": "ok", "message": "dados atualizados"}