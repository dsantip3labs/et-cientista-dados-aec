from __future__ import annotations
import re
from pathlib import Path
from typing import Any, List, Optional
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

_ESPACAO_BRANCO_RE = re.compile(r"\s+")
_NON_PRINTABLE_RE = re.compile(r"[\x00-\x1F\x7F]")
_MININO_CATG = 20

def normalizar_texto(text: str) -> str:
    if text is None:
        return ""
    text = str(text)
    text = _NON_PRINTABLE_RE.sub(" ", text)
    text = _ESPACAO_BRANCO_RE.sub(" ", text)
    return text.strip()

def juncao_texto_titulo(title: str, text: str) -> str:
    title_n = normalizar_texto(title)
    text_n = normalizar_texto(text)
    if title_n and text_n:
        return f"{title_n}. {text_n}"
    return title_n or text_n

def build_text_series(df: pd.DataFrame) -> pd.Series:
    return df.apply(lambda r: juncao_texto_titulo(r["title"], r["text"]), axis=1)

def min_catg(dados: pd.DataFrame, coluna: str = "category", min_count: int = _MININO_CATG) -> pd.DataFrame:
    total = dados[coluna].value_counts()
    categorias_validas = total[total >= min_count].index
    dados_final = dados[dados[coluna].isin(categorias_validas)].copy()
    return dados_final

def savar_modelo(model: Any, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)

def carregar_modelo(path: str | Path) -> Any:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Modelo nao encontrado: {path}")
    return joblib.load(path)

def evaluate_predictions(y_true, y_pred) -> str:
    return classification_report(y_true, y_pred, digits=4)

def confusion(y_true, y_pred, labels: Optional[List[str]] = None):
    return confusion_matrix(y_true, y_pred, labels=labels)

def sample_errors(
    df: pd.DataFrame,
    y_true,
    y_pred,
    proba=None,
    top_n: int = 10,
    text_max: int = 220,
) -> pd.DataFrame:
    rows = []
    for i, (t, p) in enumerate(zip(y_true, y_pred)):
        if t != p:
            text = juncao_texto_titulo(df.iloc[i]["title"], df.iloc[i]["text"])
            snippet = (text[:text_max] + "...") if len(text) > text_max else text
            row = {"idx": i, "true": t, "pred": p, "snippet": snippet}
            if proba is not None:
                row["pred_confidence"] = float(max(proba[i]))
            rows.append(row)
    return pd.DataFrame(rows).head(top_n)