from flask import Flask, request, jsonify
from flask_cors import CORS 
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Load variables from .env
load_dotenv()

# 2. Configure AI Model
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("CRITICAL ERROR: GOOGLE_API_KEY not found in environment!")
else:
    genai.configure(api_key=api_key)

app = Flask(__name__)

# 3. ENHANCED CORS setup
# This tells the browser: "I allow GitHub Pages to talk to me."
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}}) 

model = genai.GenerativeModel('gemini-pro')

@app.route("/", methods=["GET"])
def home():
    return "Jarvis AI Backend is Running"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    # Handle the browser "handshake" (Pre-flight)
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        user_data = request.get_json()
        if not user_data:
            return jsonify({"response": "Error: No data received"}), 400
            
        user_message = user_data.get("message")
        if not user_message:
            return jsonify({"response": "Error: No message provided"}), 400
        
        # Generate response using Gemini
        response = model.generate_content(user_message)
        
        if response and response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "The AI could not generate a response."})

    except Exception as e:
        print(f"AI Error: {str(e)}")
        return jsonify({
            "response": f"I'm sorry, I'm having trouble thinking. (Error: {str(e)})"
        }), 500

if __name__ == "__main__":
    # 0.0.0.0 is critical for Kubernetes routing
    app.run(host="0.0.0.0", port=8000)
