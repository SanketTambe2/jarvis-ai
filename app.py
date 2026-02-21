from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Make sure your GOOGLE_API_KEY is set in your environment or Secret
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
CORS(app)  # This is the "bridge" that lets GitHub Pages talk to your local Minikube

model = genai.GenerativeModel('gemini-pro')

@app.route("/")
def home():
    return "Jarvis Backend is Running"

@app.route("/chat", methods=["POST"])
def chat():
    user_data = request.json
    user_message = user_data.get("message")
    
    try:
        # This calls the actual AI
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "AI could not process this request"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
