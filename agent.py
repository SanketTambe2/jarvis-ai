from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return "Jarvis Backend Running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message","")

    reply = f"Jarvis says: {message}"

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
