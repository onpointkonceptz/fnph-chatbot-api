from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# 🔄 Load API key from .env
load_dotenv()

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GOOGLE_AI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    f"?key={GOOGLE_API_KEY}"
)

@app.route("/", methods=["GET"])
def home():
    return "✅ Home route works!"

@app.route("/test", methods=["GET"])
def test():
    return "✅ Test route works!"

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    payload = {"contents": [{"parts": [{"text": user_message}]}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(GOOGLE_AI_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply})
    except requests.exceptions.HTTPError as http_err:
        print("🔴 HTTP Error:", http_err)
        return jsonify({"reply": f"API error: {response.text}"}), 500
    except Exception as err:
        print("🔴 General Error:", err)
        return jsonify({"reply": f"Unexpected error: {str(err)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
