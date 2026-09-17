from __future__ import annotations

import os
import xml.etree.ElementTree as ET
import re
import httpx

DEFAULT_GROBID_URL = "http://localhost:8070"

def _clean_sentence(text: str) -> str:
    # REMOVE CR/LF (LINE BREAKS)
    text = "".join(text.splitlines())

    # Handle edge case -> urls in line breaks: http://scholia. toolforge.org →  http://scholia.toolforge.org
    text = re.sub(r"(https?://.*?)\.\s+(\S+)", r"\1.\2", text)
    return " ".join(text.split())


class GrobidError(Exception):
    """Raised when the GROBID container cannot process a PDF."""

class GrobidService:
    """Thin client for the GROBID REST API (docker compose service `grobid`)."""

    def __init__(self, base_url: str | None = None, timeout_seconds: float = 90.0) -> None:
        self.base_url = (base_url or os.environ.get("GROBID_URL") or DEFAULT_GROBID_URL).rstrip("/")
        self.timeout_seconds = timeout_seconds


    """POST a PDF to `/api/processFulltextDocument` and return TEI XML."""
    async def process_fulltext(self, pdf_bytes: bytes, filename: str = "document.pdf", *, segment_sentences: bool = True,
    ) -> str:
        url = f"{self.base_url}/api/processFulltextDocument"
        files = {"input": (filename, pdf_bytes, "application/pdf")}
        data = {"segmentSentences": "1" if segment_sentences else "0"}
        timeout = httpx.Timeout(self.timeout_seconds)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, files=files, data=data)

        if response.status_code != 200:
            raise GrobidError(
                f"GROBID returned HTTP {response.status_code}: {response.text[:500]}"
            )
        return response.text


    
    def sentences_from_tei(self, tei_xml: str) -> list[str]:
        root = ET.fromstring(tei_xml)
        ns = {"tei": "http://www.tei-c.org/ns/1.0"}
        sentences = []

        for s in root.findall(".//tei:s", ns):
            cleaned = _clean_sentence("".join(s.itertext()))
            if cleaned:
                sentences.append(cleaned)
        return sentences


grobid = GrobidService()
