import os
import sys
from pathlib import Path

os.environ.setdefault("GROBID_URL", "http://localhost:8070")

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from main import app

client = TestClient(app)
PDF_PATH = Path(__file__).resolve().parents[2] / "ui" / "2303.15133.pdf"


def test_01():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_02():
    with open(PDF_PATH, "rb") as f:
        response = client.post(
            "/v1/extract-sentences",
            files={"pdf_file": ("2303.15133.pdf", f, "application/pdf")},
        )

    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data["sentences"], list)
    assert len(data["sentences"]) > 0
    assert "How language should best be handled is not clear." in data["sentences"]


if __name__ == "__main__":
    test_01()
    test_02()
    print("All tests passed!")
