from flask import Flask, jsonify
import os

app = Flask(__name__)

# Assign a unique server ID
SERVER_ID = os.getenv("SERVER_ID", "Server 2")

@app.route("/")
def handle_request():
    return jsonify({
        "message": f"Request handled by {SERVER_ID}"
    })

if __name__ == "__main__":
    # Run the server on a specified port
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5002)))
