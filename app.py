from dotenv import load_dotenv
import os
import requests
import json
from flask import Flask, render_template, request, jsonify
import base64

dotenv_path = "/Users/msayn47painter/Desktop/IBM AI CERTIFICATE/App with Flask/IBMAPP_Repo/zzrjt-practice-project-emb-ai/.env"
load_dotenv(dotenv_path)

TTS_API_KEY = os.getenv("TTS_API_KEY")
TTS_URL = os.getenv("TTS_URL")
STT_API_KEY = os.getenv("STT_API_KEY")
STT_URL = os.getenv("STT_URL")
NLU_API_KEY = os.getenv("NLU_API_KEY")
NLU_URL = os.getenv("NLU_URL")

if not all([TTS_API_KEY, TTS_URL, STT_API_KEY, STT_URL, NLU_API_KEY, NLU_URL]):
    raise ValueError("One or more environment variables aren't loaded properly.")


app = Flask(__name__)

@app.route("/sentiment_analyser", methods=["POST"])
def sentiment_analyser():
    """ Analyse de sentiment avec IBM Watson NLU """
    data = request.get_json()
    text_to_analyse = data.get("text") if data else request.form.get("text")

    if not text_to_analyse or text_to_analyse.strip() == "":
        return jsonify({"error": "Invalid input! Try again."}), 400

    auth_header = base64.b64encode(f"apikey:{NLU_API_KEY}".encode()).decode()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_header}"
    }

    input_json = {
        "text": text_to_analyse,
        "features": {"sentiment": {}},
    }

    response = requests.post(f"{NLU_URL}/v1/analyze?version=2021-08-01", json=input_json, headers=headers)

    if response.status_code != 200:
        return jsonify({"Invalid input! Try again."}), 400

    response_json = response.json()
    label = response_json.get("sentiment", {}).get("document", {}).get("label")
    score = response_json.get("sentiment", {}).get("document", {}).get("score")

    if not label:
        return jsonify({"error": "Invalid input! Try again."}), 400

    return jsonify({
        "label": label,
        "score": score
    })

@app.route("/")
def render_index_page():
    """ Affiche la page principale """
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
