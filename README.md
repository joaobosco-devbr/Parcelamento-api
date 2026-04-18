# Parcelamento API

API REST para simulacao de parcelamento de divida com regras fixas de juros por quantidade de parcelas.

O projeto expoe um endpoint para calcular o valor total da divida, juros aplicados e valor de cada parcela, com validacao de entrada, arredondamento monetario com duas casas decimais e testes automatizados.

## Descricao do projeto

Esta aplicacao foi construida com FastAPI para fornecer uma interface simples de simulacao de parcelamento. O foco do projeto e concentrar as regras de negocio de forma clara, manter a logica de calculo isolada em funcao pura e garantir previsibilidade por meio de testes automatizados.

## Tecnologias utilizadas

- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- Docker
- Docker Compose

## Estrutura do projeto

```text
parcelamento-api/
|-- app/
|   |-- main.py
|   |-- rules.py
|   |-- schemas.py
|   |-- routers/
|   |   |-- health.py
|   |   `-- simulacao.py
|   `-- services/
|       `-- parcelamento.py
|-- tests/
|   |-- test_api.py
|   `-- test_service.py
|-- .dockerignore
|-- docker-compose.yml
|-- Dockerfile
|-- pytest.ini
|-- requirements-dev.txt
|-- requirements.txt
`-- README.md
```

## Regras de negocio

- `valor_divida` deve ser maior que zero.
- `parcelas` permitidas: `1`, `3`, `6`, `9` e `12`.
- As taxas de juros sao fixas por quantidade de parcelas:

| Parcelas | Juros (%) |
|----------|-----------|
| 1        | 0.0       |
| 3        | 10.0      |
| 6        | 15.0      |
| 9        | 20.0      |
| 12       | 25.0      |

- O calculo usa arredondamento monetario com duas casas decimais.
- A logica de calculo esta separada em funcao pura para facilitar teste e manutencao.

## Como rodar localmente

### 1. Instalar dependencias

Para executar apenas a aplicacao:

```bash
pip install -r requirements.txt
```

Para desenvolvimento e testes:

```bash
pip install -r requirements-dev.txt
```

### 2. Variaveis de ambiente

Atualmente a aplicacao nao exige variaveis de ambiente obrigatorias para execucao.

### 3. Iniciar a aplicacao

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Acessar a API

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Como rodar com Docker

### 1. Gerar a imagem

```bash
docker build -t parcelamento-api .
```

### 2. Subir o container

```bash
docker run -p 8000:8000 parcelamento-api
```

### 3. Variaveis de ambiente no container

No estado atual do projeto, nenhuma variavel de ambiente e obrigatoria.

### 4. Acessar a aplicacao

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

## Como rodar com Docker Compose

### 1. Subir a aplicacao

```bash
docker compose up --build
```

### 2. Acessar a aplicacao

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

## Como executar testes

```bash
pip install -r requirements-dev.txt
pytest
```

Se o terminal atual ainda nao reconhecer `pytest`, abra uma nova sessao do terminal apos a instalacao das dependencias.

## Exemplo de request e response

### Request

`POST /simular`

```json
{
  "valor_divida": 1000.0,
  "parcelas": 6
}
```

### Response

```json
{
  "valor_original": 1000.0,
  "juros_percentual": 15.0,
  "valor_juros": 150.0,
  "valor_total": 1150.0,
  "parcelas": 6,
  "valor_parcela": 191.67
}
```

## Endpoint Swagger

A documentacao interativa da API esta disponivel em:

```text
http://localhost:8000/docs
```
