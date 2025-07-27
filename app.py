import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get your API key from environment variable
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Correct model name
MODEL_NAME = "models/gemini-1.5-pro-002"

# Correct Gemini API endpoint
GOOGLE_AI_URL = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent?key={GOOGLE_API_KEY}"

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"reply": "Please provide a message"}), 400

        payload = {
            "contents": [
                {
                    "parts": [{"text": user_message}]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(GOOGLE_AI_URL, headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            try:
                ai_reply = response_data["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify({"reply": ai_reply})
            except (KeyError, IndexError):
                return jsonify({"reply": "Sorry, I couldn't understand the response from Gemini."}), 500
        else:
            return jsonify({"reply": f"API error: {response.text}"}), 500

    except Exception as e:
        return jsonify({"reply": f"Internal server error: {str(e)}"}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
