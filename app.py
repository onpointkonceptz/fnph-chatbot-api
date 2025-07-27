from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Load your API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Correct Gemini Pro endpoint (v1beta)
GOOGLE_AI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    f"?key={GOOGLE_API_KEY}"
)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "No message provided."}), 400

    payload = {
        "contents": [
            {
                "parts": [{"text": user_message}]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(GOOGLE_AI_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply})
    except requests.exceptions.HTTPError as e:
        print("🔴 HTTP error:", e)
        return jsonify({"reply": f"API error: {response.text}"}), 500
    except Exception as e:
        print("🔴 General error:", e)
        return jsonify({"reply": f"Unexpected error: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def home():
    return "✅ Chatbot backend is running!"

@app.route('/test', methods=['GET'])
def test():
    return "✅ Test route works!"

if __name__ == '__main__':
    app.run(debug=True)
