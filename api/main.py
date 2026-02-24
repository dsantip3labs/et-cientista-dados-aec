from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from api.schemas import SolicitacaoPredicao, RespostaPredicao
from src.utils import carregar_modelo
from src.predicao import predict_one
from pathlib import Path
import os
import logging


MODEL_PATH = os.getenv("MODEL_PATH", str(Path("modelo/modelo.joblib")))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pego da documentação do FastAPI, para carregar o modelo na inicialização da aplicação
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = None
    try:
        print(f"Carregando modelo em: {MODEL_PATH}")
        app.state.model = carregar_modelo(MODEL_PATH)
        print("Modelo carregado com sucesso.")
    except FileNotFoundError:
        print(f"Modelo não encontrado em {MODEL_PATH}.")
    except Exception as e:
        print(f"Erro ao carregar modelo: {e}")
    yield
    app.state.model = None

app = FastAPI(title="Classificador de Notícias", version="1.0", lifespan=lifespan)

@app.get("/teste")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=RespostaPredicao)
def predict(req: SolicitacaoPredicao):
    if app.state.model is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado.")
    try:
        return predict_one(app.state.model, title=req.title, text=req.text, top_k=req.top_k)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao predizer.")
