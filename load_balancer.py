import requests
from flask import Flask, jsonify, request
import threading
import time

app = Flask(__name__)

BACKEND_SERVERS = [
    "http://localhost:5001", 
    "http://localhost:5002"                   
]
#Adding health checks for healthy servers
healthy_servers = []

#Lock for thread safe access to healthy servers
servers_lock = threading.Lock()

current_server_index = 0

#Health-Checking function
def health_check():
    global healthy_servers
    global current_server_index

    while True:
        with servers_lock:
            new_healthy_servers = []
            for server in BACKEND_SERVERS:
                try:
                    response = requests.get(server, timeout=2)
                    if response.status_code == 200:
                        new_healthy_servers.append(server)
                except requests.exceptions.RequestException:
                    pass

            # Update the healthy_servers list
            healthy_servers = new_healthy_servers

            # Reset the current index if necessary
            if current_server_index >= len(healthy_servers):
                current_server_index = 0

        time.sleep(5)


# Start health check in a separate thread
threading.Thread(target=health_check, daemon=True).start()


@app.route("/", methods=["GET", "POST"])
def load_balance():
    global current_server_index

    if not healthy_servers:
        return jsonify({"error":"No healthy servers available"}), 503

    server_url = healthy_servers[current_server_index]
    current_server_index = (current_server_index+1)%len(healthy_servers)

    try:
        if request.method=="GET":
            response = requests.get(server_url)
        else:
            response = requests.post(server_url, json = request.get_json())
        return jsonify({
            "server": server_url,
            "response": response.json()
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Failed to reach server {server_url}",
            "details": str(e)
        }), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080)

