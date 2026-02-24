from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from src.predicao import predict_one

def _toy_model() -> Pipeline:
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=500)),
    ])
    pipe.fit(["bola gol", "juros banco"], ["esporte", "economia"])
    return pipe


# Testa a função predict_one com um modelo de brinquedo

def test_predict_one_contract():
    model = _toy_model()
    out = predict_one(model, title="Banco", text="juros", top_k=2)

    assert isinstance(out, dict)
    assert "categoria" in out
    assert out["categoria"] in {"economia", "esporte"}

    assert "top_k" in out
    assert isinstance(out["top_k"], list)
    assert len(out["top_k"]) <= 2
    print(out)