# Pq esse arquivo de notas?

Geralmente quando vou fazer um projeto gosto de organizar anteriormente todas etapas previamente para facilitar a construção. Algumas coisas que vou encontrando, pensando ou tendo ideia eu vou jogando aqui, então geralmente esse arquivo é bem bagunçado apartir de algum momento, mas me ajuda a expressar tudo e sair executando.

# Estrutura e organização mental


Prioridades:

- P0: estrutura do projeto, fazer eda, script de treino, api (avaliar qual vou usar)
- P1: métricas (dps do EDA), analise dos erros e tunning
- P2 (extras do projeto): dockerfile, pytest (vou ter que estudar mais um pouco esse aqui), documentação e pensar depois e quando tiver utilizando o que posso adicionar.

# Possiveis ferramentas

- FastAPI
- Flask - Não sei se faz sentido utilizar ela aqui, não tenho conhecimento da lib e pelo que avaliei é uma para desenvolvimento web. Vou manter tudo somente na API, se sobrar tempo estudo algo para implementar ela
- O doc pede para utilizar Spacy, sckitlearn, huggingface e nltk.


---

# Criterios de avaliação


Trouxe só para lembrar dos pontos do pdf.

O teste técnico será avaliado seguindo a ordem de importância abaixo:
1. Clareza de código: obediência à boas práticas, comentários descritivos, padronização de estilo, etc.
2. Entrega do resultado: a ideia é termos um classificador que possa ser executado como em produção,
que possamos fazer requisições e receber os resultados.
3. Modelagem: metodologia aplicada, técnicas, algoritmos e métricas utilizados.
4. EDA: resultados iniciais de análise, uso de tais resultados para modelagem

# Anotações rapidas

- Levar o avl_dados para um notebook, acho que vai ser melhor para apresentar.
- Seguir com F1 macro, desbalanceamento ficou alto e vou seguir com a remoção de algumas categorias.
- input da api vai ser o titulo da materia ou uma parte do texto.
- vou rodar local com fastapi mesmo


# Etapas

- Estrutura - OK
- EDA - feito (resumo e notebook)
- Script de treino
- Baseline - TF-IDF, Metricas e salvar modelo
- Avaliação de erros e testes
- API
- README
- Docker