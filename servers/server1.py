from flask import Flask, jsonify
import os

app = Flask(__name__)

#Here we assign a unique server ID
SERVER_ID = os.getenv("Server_ID", "Server 1")


@app.route("/")
def handle_request():
    return jsonify({
        "message" : f"Request handled by {SERVER_ID}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)))

