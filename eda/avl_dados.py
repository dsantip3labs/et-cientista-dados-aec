import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# testar o treino
from sklearn.model_selection import train_test_split

caminho = 'arquivos/articles.csv'

dados = pd.read_csv(caminho, encoding='ISO-8859-1', sep=',')

caminho = 'sample_data/articles.csv'

dados = pd.read_csv(caminho, encoding='utf-8', sep=',')

# conferindo os dados, as colunas, tipos de dados, quantidade de linhas e os dtypes.
print(dados.info())

# nulos

nulos = dados.isna().sum()
print(nulos)

print(dados.isna().mean().sort_values(ascending=False))


# vou utilizar titulo e o texto para avaliar a categoria

def linhas_vazias(col):
    s = col.fillna("").astype(str).str.strip()
    return (s == "").mean()

for c in ["title", "text"]:
    if c in dados.columns:
        print(c, linhas_vazias(dados[c]))

# duplicados

dados.duplicated().mean()

coluna = "category"
top_n = 20

contagem = dados[coluna].value_counts()

contagem.head(top_n).sort_values().plot(kind="barh")
plt.title(f"Top {top_n} categorias")
plt.show()

print("---")

ratio = contagem.max() / contagem.min()
print(f"Balanceamento: {ratio}")

# resultado daqui deu um desbalanceamento de 22k, ou seja
# a categoria mais frequente tem 22 mil de vezes mais amostras do que a menos frequente

# número até que expressivo, vou só validar se tem categorias com poucas amostras

'''
counts = dados["category"].value_counts()
counts.tail(20)
'''

# tinha categorias com 1 amostra, comentei aqui, mas vou levar para o notebook.

# para evitar categorias com poucas amostras, vou filtrar as categorias com menos de um certo número de amostras.

MIN_COUNT = 20

total = dados[coluna].value_counts()
categorias_validas = total[total >= MIN_COUNT].index

dados_final = dados[dados[coluna].isin(categorias_validas)].copy()

categorias_removidas = total[total < MIN_COUNT]
linhas_removidas = categorias_removidas.sum()

print("Categorias originais:", total.shape[0])
print("Categorias mantidas:", len(categorias_validas))
print("Categorias removidas:", categorias_removidas.shape[0])
print("Linhas removidas:", int(linhas_removidas))
print("Linhas mantidas:", dados_final.shape[0])

counts = dados_final[coluna].value_counts()

top_n = 20
counts.head(top_n).sort_values().plot(kind="barh")
plt.title(f"Top {top_n} categorias (minimo={MIN_COUNT})")
plt.show()

ratio = counts.max() / counts.min()

print("\n---\n")

print("Novo desbalanceamento:", float(ratio))
print("Min:", int(counts.min()), "| Max:", int(counts.max()))


# normalização do texto 
def norm_str(x):
    if pd.isna(x):
        return ""
    return str(x).strip()

dados_final["title_clean"] = dados_final["title"].map(norm_str) if "title" in dados_final.columns else ""
dados_final["text_clean"]  = dados_final["text"].map(norm_str)  if "text" in dados_final.columns else ""

dados_final["input_text"] = np.where(dados_final["text_clean"].str.len() > 0, dados_final["text_clean"], dados_final["title_clean"])

empty_input_rate = (dados_final["input_text"].str.len() == 0).mean()
print("Taxa de input_text vazio:", empty_input_rate)

dados_final["token_len"].clip(upper=dados_final["token_len"].quantile(0.99)).hist(bins=40)
plt.title("Distribuição de tokens (cortado no p99)")
plt.show()

# mostrar os textos mais longos e mais curtos, comentado aqui no codigo para não poluir a tela, mas vai ser documentado no notebook.

#dados_final.sort_values("token_len", ascending=False)[["input_text", coluna, "token_len"]].head(5)
#dados_final.sort_values("token_len", ascending=True)[["input_text", coluna, "token_len"]].head(5)

# definir uma função de limpeza de texto, que remove URLs, múltiplos espaços e converte para minúsculas

def clean_text(s):
    s = str(s).lower().strip()
    s = re.sub(r"http\S+|www\.\S+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# teste do treino

dados_final["input_text_clean"] = dados_final["input_text"].map(clean_text)
dados_final[["input_text", "input_text_clean"]].head(3)

X = dados_final["input_text_clean"]
y = dados_final[coluna]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Treino:", X_train.shape[0], "Teste:", X_test.shape[0])
print("Min count treino:", int(y_train.value_counts().min()))
print("Min count teste:", int(y_test.value_counts().min()))
