from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ✅ Correct Gemini-Pro endpoint (v1beta) for MakerSuite API Key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_AI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    f"?key={GOOGLE_API_KEY}"
)

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_message}
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(GOOGLE_AI_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply})
    except requests.exceptions.HTTPError as e:
        print("🔴 HTTP Error:", e)
        return jsonify({"reply": f"API error: {resp.text}"}), 500
    except Exception as e:
        print("🔴 General Error:", e)
        return jsonify({"reply": f"Unexpected error: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    return "Chatbot backend is running."

# ✅ Debug route to confirm if deployed correctly
@app.route("/test", methods=["GET"])
def test():
    return "Test route works!"
