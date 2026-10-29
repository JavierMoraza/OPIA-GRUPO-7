import os
from contextlib import asynccontextmanager

import joblib
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_PATH = "modelo_california.pkl"
# TODO: URL "raw" del modelo en TU repositorio de GitHub. Formato:
# https://raw.githubusercontent.com/<usuario>/<repositorio>/main/modelo_california.pkl
MODEL_URL = "https://raw.githubusercontent.com/JavierMoraza/OPIA-GRUPO-7/main/modelo_california.pkl"
DOWNLOAD_TIMEOUT = 30  # segundos

# El modelo se carga al arrancar y se guarda aquí.
state = {"model": None}

class HouseFeatures(BaseModel):
    """Variables de entrada del modelo (una zona censal)."""
    MedInc: float | int
    HouseAge: float | int
    AveRooms: float | int
    AveBedrms: float | int
    Population: float | int
    AveOccup: float | int
    Latitude: float | int
    Longitude: float | int

def download_model(url: str = MODEL_URL, path: str = MODEL_PATH):
    """Descarga el modelo desde `url` y lo guarda en `path`.

    Pistas: usa requests.get(url, timeout=DOWNLOAD_TIMEOUT), comprueba el
    resultado con response.raise_for_status() y escribe response.content en
    el fichero abriéndolo en modo binario ("wb").
    """
    print(f"Iniciando descarga desde {url}...")
    response = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
    response.raise_for_status()  # Lanza un error si la descarga falla

    with open(path, "wb") as f:
        f.write(response.content)
    print("Descarga completada.")

def load_model(path: str = MODEL_PATH):
    """Carga el modelo. Si no existe en local, lo descarga antes de GitHub."""
    if not os.path.exists(path):
        print(f"{path} no encontrado en local, descargando...")
        download_model()
    return joblib.load(path)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Se ejecuta una vez al arrancar el servicio."""
    state["model"] = load_model()
    yield

app = FastAPI(title="Precio de casas en California", lifespan=lifespan)

@app.get("/")
def health():
    """Health-check: confirma que el servicio está funcionando."""
    return {"status": "ok"}

@app.post("/predict")
def predict(features: HouseFeatures):
    """Devuelve el precio medio estimado (en cientos de miles de dólares)."""
    model = state["model"]
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no cargado")
    X = pd.DataFrame([features.model_dump()])
    prediction = model.predict(X)[0]
    return {"MedHouseVal": float(prediction)}
