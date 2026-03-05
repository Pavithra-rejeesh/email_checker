from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from disposable_email_detector_pro import assess_email

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return send_from_directory("/Users/buymeacoffee/Documents/email_checker", "index.html")

@app.route("/check-email", methods=["POST"])
def check_email():
    data = request.json

    if not data or "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    email = data.get("email").strip()

    result = assess_email(email)

    return jsonify(result)


if __name__ == "__main__":
    app.run(port=3001, debug=True)