from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get your Gemini API key
API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini
genai.configure(api_key=API_KEY)

# Use Gemini Pro model
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return jsonify({"message": "FNPH Chatbot API is running"}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        response = model.generate_content(user_message)
        reply = response.text

        return jsonify({'reply': reply})

    except Exception as e:
        return jsonify({'reply': f'API error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
