from flask import Flask, request, jsonify
from flask_cors import CORS 
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load variables from .env if running locally
load_dotenv()

# Configure AI Model
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("CRITICAL ERROR: GOOGLE_API_KEY not found in environment!")
else:
    genai.configure(api_key=api_key)

app = Flask(__name__)

# CORS setup: allows your GitHub Pages frontend to talk to this backend
CORS(app, resources={r"/*": {"origins": "*"}}) 

model = genai.GenerativeModel('gemini-pro')

@app.route("/", methods=["GET"])
def home():
    return "Jarvis AI Backend is Running"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    # Handle the 'pre-flight' request from the browser
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    user_data = request.json
    if not user_data:
        return jsonify({"response": "Error: No data received"}), 400
        
    user_message = user_data.get("message")
    
    if not user_message:
        return jsonify({"response": "Error: No message provided"}), 400
    
    try:
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"AI Error: {str(e)}")
        return jsonify({"response": f"I'm sorry, I'm having trouble thinking right now. (Error: {str(e)})"}), 500

if __name__ == "__main__":
    # Port 8000 is used to match your Kubernetes port-forwarding
    app.run(host="0.0.0.0", port=8000)
