# README - Etapa tecnica - Cientista de dados jr - AeC

Esta é a documentação para o projeto. Inclui:

- Guia de instalação e utilização
- Execução local
- Docker compose

## Objetivo

Rodar localmente, fazer solicitação em HTTP (localhost) e receber categoria + top-k.

### Conjunto de dados

- Kaggle: https://www.kaggle.com/datasets/marlesson/news-of-the-site-folhauol


## Requisistos

- Python | Minimo >= 13.1
- Git (opcional)
- Docker (opcional)
- Porta 8000 livre (quando usado o docker)

## Libs utilizadas

- pandas
- numpy
- scikit-learn
- matplotlib
- kagglehub
- matplotlib
- joblib
- pytest
- fastapi
- uvicorn

## Rodando com Docker Compose

Por limite de tamanho, o arquivo do modelo não vem no repo.

Faça download desse repositorio diretamente no github ou faça um clone com git.

`git clone https://github.com/dsantip3labs/et-cientista-dados-aec.git`


### Subir a aplicação

`docker compose up --build`

- Modelo irá ser baixado automaticamente via github.

## Instalação local

> Execute no cmd

Faça download desse repositorio diretamente no github ou faça um clone com git.

`git clone https://github.com/dsantip3labs/et-cientista-dados-aec.git`

Instale as dependencias via requirements.

- `pip install -r requirements.txt`

## Download dos dados

Por limitação do github, arquivos com mais de 100mb não sobem para o repisotorio.
Resolvemos isso incluindo um script para download da base de dados do kaggle direto na pasta de arquivos.

> Execute na pasta raiz do projeto

`python script_downloadcsv.py`

## Configuração do modelo

Confirme que o arquivo "articles.csv" está na pasta /arquivos. Após isso, pelo mesmo problema do tamanho do arquivo iremos gerar localmente novamente o arquivo de modelo.

`python -m src.treino_modelo --csv .\arquivos\articles.csv`

Aguarde o retorno de modelo salvo.

## Produção

Vamos colocar o projeto em produção com FastAPI e uvicorn:

> Iniciar o aplicativo

- `uvicorn api.main:app`

> Obs: Caso queira alterar algo no arquivo e não precise reiniciar o app, adicione `--reaload` no final do comando.

No cmd, aguarde o retorno de 'Application startup complete.'

## Utilização e teste da API

### Via documentação da API

- Acesse localmente na web o documento da API:  `localhost:8080/docs`
- Acesse o POST /predict
- Aperte o botão "Try it out"
- Edite o schema conforme desejar adicionando o título da noticia ou texto
- Exceute e encontre o resultado na aba de "Server response"

### Via Curl

Ajuste o curl com título ou texto.
`
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "",
  "text": "",
  "top_k": 3
}' `