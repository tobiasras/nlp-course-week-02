from flask import Flask, jsonify, request
from afinn import Afinn

app = Flask(__name__)

afinn_en = Afinn(language="en")
afinn_da = Afinn(language="da")


@app.get("/")
def root():
    return jsonify({"message": "app is running good:)"})


@app.post("/v1/sentiment")
def analyze_sentiment():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    score_en = afinn_en.score(text)
    score_dk = afinn_da.score(text)
    score = (score_dk + score_en) / 2
    return jsonify({"score": score})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
