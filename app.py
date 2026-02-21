from flask import Flask, request, jsonify
from flask_cors import CORS 
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration from Environment Variables (Secrets)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
CORS(app) 

model = genai.GenerativeModel('gemini-pro')

@app.route("/")
def home():
    return "Jarvis AI Backend is Running"

@app.route("/chat", methods=["POST"])
def chat():
    user_data = request.json
    user_message = user_data.get("message")
    
    if not user_message:
        return jsonify({"error": "No message"}), 400
    
    try:
        # Simple AI Chat Logic
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
