import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import json


load_dotenv()

#Banco de dados

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

def get_sheet():
    
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
    ]

    creds_info = json.loads(os.environ["GOOGLE_CREDS"])

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

# =========================
# FASTAPI
# =========================

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API de Passagens"}

@app.on_event("startup")
def startup_event():
    print("Iniciando a sincronização inicial...")
    sync_all()
    print("Sincronização inicial concluída!")

@app.get("/sync")
def sync():
    sync_all()
    return {"message": "Sincronização concluída!"}
