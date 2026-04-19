# Parcelamento API

API REST para simulacao de parcelamento de divida com regras versionadas de juros por faixa de parcelas.

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
- `parcelas` permitidas: de `1` a `24`.
- As taxas de juros sao fixas por faixa de parcelas:

| Parcelas | Juros (%) |
|----------|-----------|
| 1        | 0.0       |
| 2 a 3    | 10.0      |
| 4 a 6    | 15.0      |
| 7 a 9    | 20.0      |
| 10 a 12  | 25.0      |
| 13 a 15  | 30.0      |
| 16 a 18  | 35.0      |
| 19 a 21  | 40.0      |
| 22 a 24  | 45.0      |

- O calculo usa arredondamento monetario com duas casas decimais.
- A logica de calculo esta separada em funcao pura para facilitar teste e manutencao.
- A configuracao do produto fica versionada em `app/config/parcelamento.v1.json`.
- A API expoe `versao_configuracao` no `health` e na resposta da simulacao.
- As rotas publicas estao versionadas em `/api/v1`.
- Os erros da API seguem um contrato padronizado com `code`, `message` e `details`.

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

### 2. Configuracao do produto

As regras de parcelamento ficam centralizadas no arquivo versionado:

```text
app/config/parcelamento.v1.json
```

Esse arquivo define:

- intervalo minimo e maximo de parcelas
- tabela de juros por limite superior
- versao da configuracao aplicada pela API

Atualmente a aplicacao nao exige variaveis de ambiente obrigatorias para execucao.

### 3. Iniciar a aplicacao

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Acessar a API

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

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

`POST /api/v1/simular`

```json
{
  "valor_divida": 1000.0,
  "parcelas": 6
}
```

### Response

```json
{
  "versao_configuracao": 1,
  "valor_original": 1000.0,
  "juros_percentual": 15.0,
  "valor_juros": 150.0,
  "valor_total": 1150.0,
  "parcelas": 6,
  "valor_parcela": 191.67
}
```

### Health

`GET /api/v1/health`

```json
{
  "status": "ok",
  "produto": "parcelamento",
  "versao_configuracao": 1
}
```

## Padrao de erro

Exemplo de erro de validacao:

```json
{
  "code": "validation_error",
  "message": "Dados de entrada invalidos",
  "details": [
    {
      "field": "parcelas",
      "message": "Value error, parcelas deve estar entre 1 e 24"
    }
  ]
}
```

## Endpoint Swagger

A documentacao interativa da API esta disponivel em:

```text
http://localhost:8000/docs
```
