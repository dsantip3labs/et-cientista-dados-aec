from __future__ import annotations
import argparse
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from src.data import carregar_dados
from src.utils import build_text_series, evaluate_predictions, savar_modelo, sample_errors, min_catg


# referencia para pipeline e modelo pega direto dos documents do sklearn

def build_pipeline() -> Pipeline:
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=20,
        max_df=0.95,
        strip_accents="unicode",
    )
    clf = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
    )
    return Pipeline([("tfidf", vectorizer), ("clf", clf)])

def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--model-out", default="modelo/modelo.joblib")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    dados = min_catg(carregar_dados(args.csv))

    X = build_text_series(dados)

    y = dados["category"]

    X_train, X_test, y_train, y_test, df_train, df_test = train_test_split(
        X, y, dados, test_size=args.test_size, random_state=args.seed, stratify=y
    )

    pipe = build_pipeline()

    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)

    proba = pipe.predict_proba(X_test) if hasattr(pipe, "predict_proba") else None

    print("Relatorio de classificacao:\n")
    print(evaluate_predictions(y_test, y_pred))
    print("Exemplos de erro (top 10):\n")
    print(sample_errors(df_test.reset_index(drop=True), y_test.reset_index(drop=True), y_pred, proba=proba))

    savar_modelo(pipe, args.model_out)
    print(f"\nModelo salvo em: {Path(args.model_out).resolve()}")

if __name__ == "__main__":
    main()