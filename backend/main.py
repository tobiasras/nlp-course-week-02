from fastapi import FastAPI, File, HTTPException, UploadFile
import uvicorn
import logging

from grobid import GrobidError, grobid

app = FastAPI()
log = logging.getLogger("uvicorn.error")


@app.get("/")
async def root():
    return {"message": "app is running good:)"}


@app.post("/v1/extract-sentences")
async def extract_sentences(pdf_file: UploadFile = File(...)):

    if pdf_file.filename is None:
        raise HTTPException(status_code=400)

    pdf_bytes = await pdf_file.read()

    try:
        tei_xml = await grobid.process_fulltext(pdf_bytes, pdf_file.filename or "document.pdf")
    except GrobidError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    sentences = grobid.sentences_from_tei(tei_xml)

    return {"sentences": sentences}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
