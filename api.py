from fastapi import FastAPI
from sync import sync_all

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