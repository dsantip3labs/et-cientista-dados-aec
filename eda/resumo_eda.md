# EDA — Resumo (articles.csv | Folha/UOL)

## 1) Objetivo do notebook
- Avaliar **qualidade dos dados** (nulos, vazios, duplicados, tipos).
- Entender a **distribuição de categorias** e o nível de desbalanceamento.
- Definir decisões para tornar o dataset **treinável** e a entrega **produtizável**.

> Observação: o notebook foi feito para ser **enxuto** e focado em decisões. O projeto completo (código/README/API) está no repositório: `github.com/dsantip3labs/et-cientista-dados-aec`.

---

## 2) Visão geral do dataset
- **Linhas:** 167.053  
- **Colunas:** 6  
- **Tipos:** todas as colunas estão como `object` (strings)

**Colunas**
- `title`, `text`, `date`, `category`, `subcategory`, `link`

---

## 3) Qualidade dos dados
### Nulos / vazios
- `subcategory`: 137.418 nulos (**≈82,26%**)
- `text`: 765 nulos (**≈0,46%**)
- `title`, `date`, `category`, `link`: **0 nulos**

### Duplicados
- Não foram identificadas linhas duplicadas na checagem do notebook.

### Decisão
- **Não remover** linhas com `text` vazio/nulo, porque o input pode usar **`title` como fallback**.

---

## 4) Distribuição de categorias e desbalanceamento
- Categorias originais: **48**
- Foi medido um desbalanceamento inicial muito alto (**ratio ≈ 22.022x**) por conta de categorias extremamente raras (ex.: categorias com 1–2 exemplos).
- Exemplo de “cauda longa”: existiam categorias com apenas **1 ocorrência** (ex.: `2015`, `2016`, `musica`).

### Interpretação
- Categorias com poucos exemplos **não ensinam padrão** ao modelo e tendem a gerar:
  - previsões “alucinadas”/instáveis,
  - métricas pouco confiáveis,
  - dificuldade de validação justa.

---

## 5) Filtro de classes (estabilidade)
### Regra aplicada
- Manter apenas categorias com **pelo menos 20 exemplos** (`MIN_COUNT = 20`).

### Resultado do filtro
- Categorias mantidas: **39**
- Categorias removidas: **9**
- Linhas removidas: **51**
- Linhas finais: **167.002**

### Novo desbalanceamento (após filtro)
- **Min:** 21 | **Max:** 22.022  
- **Novo ratio (max/min): ≈ 1.048,67x**

> Nota: o dataset ainda é bem desbalanceado, mas foi eliminado o “ruído extremo” das categorias com 1–2 registros.

---

## 6) Construção do texto de entrada (input_text)
Objetivo: garantir que **toda linha tenha texto** para treinar/inferir.

**Regra do input**
- Se `text` existe e não está vazio → usa `text`
- Caso contrário → usa `title`

### Verificação
- Taxa de `input_text` vazio após regra: **0%**

---

## 7) Tamanho do texto (tokens) e outliers
- Foi analisada a distribuição do tamanho do texto por **número de tokens** (`token_len`).
- Para visualização justa, o histograma foi “cortado” no **p99** (para reduzir efeito de outliers).

### Objetivo dessa checagem
- Entender se o dataset tem textos muito longos/ruidosos.
- Confirmar se um pré-processamento simples seria suficiente para um baseline de NLP clássico (ex.: TF-IDF + modelo linear).

---

## 8) Pré-processamento aplicado (limpeza mínima)
A limpeza foi propositalmente conservadora, removendo apenas ruídos óbvios:
- lowercase
- remoção de URLs
- normalização de espaços

Motivo: melhorar consistência sem “matar” informação útil do texto.

---

## 9) Separação treino/teste
- Split com **proporção 80/20** e **estratificação por classe**.
- **Treino:** 133.601  
- **Teste:** 33.401  

### Observação importante
Mesmo com `MIN_COUNT = 20`, após o split algumas classes ficaram com poucos exemplos em cada partição:
- mínimo por classe no treino: **17**
- mínimo por classe no teste: **4**

Isso pode deixar métricas por classe mais instáveis para as classes menores (algo esperado em datasets desbalanceados).

---

## 10) Decisões finais consolidadas
- **Filtro de classes:** manter apenas categorias com **≥ 20** exemplos.
- **Texto usado:** `input_text` com fallback **`text > title`**.
- **Pré-processamento:** limpeza mínima (lowercase, remover URLs, normalizar espaços).
- **Métrica principal para avaliação do modelo:** **F1 macro** (adequada para desbalanceamento).

