# PDF to sentences

A small pipeline that takes a PDF, extracts the body text, and returns a list of sentences.

Three Docker services work together:

- **GROBID** (`:8070`) converts the PDF to TEI XML with sentence segmentation
- **API** (`:8000`) FastAPI service that wraps GROBID
- **UI** (`:8001`) simple upload page to try the API in a browser

The API endpoint is `POST /v1/extract-sentences` with a form field `pdf_file`. It responds with JSON:

```json
{ "sentences": ["First sentence.", "Second sentence."] }
```

## Run

```bash
docker compose up --build
```

Then open http://localhost:8001 or call the API:

```bash
curl -s -F pdf_file=@ui/2303.15133.pdf http://localhost:8000/v1/extract-sentences
```

## Tests

GROBID must be running on `localhost:8070`.

```bash
python3 -m pytest test/backend/test_main.py
```
