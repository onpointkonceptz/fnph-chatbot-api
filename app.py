from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_AI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    f"?key={GOOGLE_API_KEY}"
)

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    payload = {"contents": [{"parts": [{"text": user_message}]}]}
    headers = {"Content-Type": "application/json"}

    resp = requests.post(GOOGLE_AI_URL, json=payload, headers=headers)
    if resp.ok:
        reply = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": "Sorry, something went wrong."}), 500

@app.route("/", methods=["GET"])
def home():
    return "Chatbot backend is running."
