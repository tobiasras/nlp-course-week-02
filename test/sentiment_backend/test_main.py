import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "sentiment_backend"))
from main import app

client = app.test_client()


def test_positive_sentiment():
    response = client.post("/v1/sentiment", json={"text": "Det var en god lærer."})
    assert response.status_code == 200
    assert response.get_json()["score"] > 0


def test_negative_sentiment():
    response = client.post("/v1/sentiment", json={"text": "It was a bad course"})
    assert response.status_code == 200
    assert response.get_json()["score"] < 0


if __name__ == "__main__":
    test_positive_sentiment()
    test_negative_sentiment()
    print("All tests passed!")
