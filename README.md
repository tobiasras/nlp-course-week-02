# NLP / LLMOps / Knowledge Graphs — Week 02

This repository is from the course **Natural language processing, large language model operations and knowledge graphs**, week 02.

The assignment is a bilingual (English and Danish) sentiment analysis Flask service for short DTU course evaluations.

## What is in this repo

| Path | Description |
| --- | --- |
| `sentiment_backend/` | Flask service that scores text with [AFINN](https://github.com/fnielsen/afinn) (English and Danish lexicons). |
| `test/sentiment_backend/` | Basic API tests for positive and negative examples. |
| `docker-compose.yml` | Runs the Flask API. |

The API contract is:

- **POST** `/v1/sentiment`
- Request: `{"text": " "}`
- Response: `{"score":}`

The backend averages the English and Danish AFINN scores.

## How to run

### Docker (recommended)

From the project root:

```bash
docker compose up --build
```

Then open:

- API: http://localhost:8000

Stop with `Ctrl+C`, or `docker compose down`.

### Tests

With the backend dependencies installed:

```bash
pip install -r sentiment_backend/requirements.txt
python test/sentiment_backend/test_main.py
```

### Run without Docker

```bash
pip install -r sentiment_backend/requirements.txt
flask --app sentiment_backend/main run --host 0.0.0.0 --port 8000
```
