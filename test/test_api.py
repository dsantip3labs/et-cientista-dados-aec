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

def test_predict_one_contract():
    model = _toy_model()
    out = predict_one(model, title="Banco", text="juros", top_k=2)
    assert "categoria" in out