from pathlib import Path
import pandas as pd

colunas = ["title", "text", "date", "category", "subcategory", "link"]

def carregar_dados(csv_path, encoding="utf-8", sep=",", dropna=True):
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {path}")

    df = pd.read_csv(path, encoding=encoding, sep=sep)

    # deixa os nomes das colunas padronizados
    df.columns = [c.strip().lower() for c in df.columns]

    missing = [c for c in colunas if c not in df.columns]
    if missing:
        raise ValueError(
            f"Faltam colunas obrigatórias: {missing}. "
            f"Colunas disponíveis: {list(df.columns)}"
        )

    # pega só o que importa e mantém a ordem
    df = df[colunas].copy()

    # troca possiveis nan por string vazia 
    if dropna:
        df = df.fillna("")

    # garantir que tudo é string 
    for col in colunas:
        df[col] = df[col].astype(str)

    return df