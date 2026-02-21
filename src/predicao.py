from __future__ import annotations
import argparse
from typing import Any, Dict
import numpy as np
from src.utils import load_model, join_title_text

# utilitário para fazer predições com o modelo treinado, a partir de título e texto
# referencia pega direto dos documents do sklearn, adaptada pra esse caso

# def para a API

def predict_one(model: Any, *, title: str = "", text: str = "", top_k: int = 3) -> Dict[str, Any]:
    final_text = join_title_text(title, text)
    pred = model.predict([final_text])[0]
    result: Dict[str, Any] = {"category": str(pred), "confidence": None, "top_k": []}
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba([final_text])[0]
        classes = model.classes_
        idx = np.argsort(proba)[::-1][:top_k]
        result["confidence"] = float(max(proba))
        result["top_k"] = [(str(classes[i]), float(proba[i])) for i in idx]
    return result

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="modelo/modelo.joblib")
    parser.add_argument("--title", default="")
    parser.add_argument("--text", default="")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()
    model = load_model(args.model)
    print(predict_one(model, title=args.title, text=args.text, top_k=args.top_k))

if __name__ == "__main__":
    main()