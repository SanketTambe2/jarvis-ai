from flask import Flask, request, jsonify
from flask_cors import CORS 
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load variables from .env
load_dotenv()

# 2. Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
else:
    print("CRITICAL ERROR: GOOGLE_API_KEY not found!")

app = Flask(__name__)

# 3. ULTIMATE CORS CONFIGURATION
# This allows GitHub Pages (or any origin) to send POST requests with JSON headers
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

@app.route("/", methods=["GET"])
def home():
    return "Jarvis AI Backend is Running"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    # Handle the browser's "handshake" check
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        user_data = request.get_json()
        if not user_data or "message" not in user_data:
            return jsonify({"response": "Error: No message received"}), 400
            
        user_message = user_data.get("message")
        
        # Generate response using Gemini
        response = model.generate_content(user_message)
        
        if response and response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "AI could not process this request."})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"response": f"Backend Error: {str(e)}"}), 500

if __name__ == "__main__":
    # host 0.0.0.0 is mandatory for Kubernetes/Docker
    app.run(host="0.0.0.0", port=8000)
