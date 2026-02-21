from typing import List, Optional
from pydantic import BaseModel, Field

class SolicitacaoPredicao(BaseModel):
    title: str = Field("", description="Título da notícia")
    text: str = Field("", description="Texto completo da notícia")
    top_k: int = Field(3, ge=1, le=10, description="Quantidade de classes retornadas no top-k")

class TopKItem(BaseModel):
    label: str
    score: float

class RespostaPredicao(BaseModel):
    categoria: str
    confidence: Optional[float] = None
    top_k: List[TopKItem] = []