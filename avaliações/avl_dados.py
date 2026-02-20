import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import collections.counter as counter
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Começar a avaliação e leitura do arquivo. Vou fazer tudo direto do kaggle mesmo,
# sem fazer download do arquivo, para evitar problemas de caminho. E a pessoa que for avaliar, pode simplesmente rodar o código e ver os resultados,
# sem precisar se preocupar com o download do arquivo.

#Retirado da documentação do kaggle, eles recomendam usar o seguinte código para ler o arquivo:

file_path = "articles.csv"

# Load the latest version
df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "marlesson/news-of-the-site-folhauol",
  file_path,
)

print("First 5 records:", df.head())