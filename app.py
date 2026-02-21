from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
# Import your logic from agent.py
from agent import Assistant 

app = Flask(__name__)
CORS(app) # Crucial for GitHub Pages to talk to your server

@app.route("/")
def home():
    return "Jarvis AI Backend is Live"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    
    # Simple logic to trigger your Assistant response
    # Note: LiveKit agents usually use WebSockets/WebRTC, 
    # but for a standard web browser chat, we return text.
    response_text = f"Jarvis received: {user_message}. (AI Logic Integrated)"
    
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
