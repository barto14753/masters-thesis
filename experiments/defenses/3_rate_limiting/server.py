from flask import Flask, request, jsonify
import time
import ollama
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(message)s")

RATE_LIMIT = 5  # Max requests per IP per minute
requests_log = {}

def is_rate_limited(ip):
    now = time.time()
    window = 60  # 1 minute window

    if ip not in requests_log:
        requests_log[ip] = []

    # Remove outdated requests
    requests_log[ip] = [t for t in requests_log[ip] if now - t < window]

    if len(requests_log[ip]) >= RATE_LIMIT:
        logging.warning(f"Rate limit exceeded for IP: {ip}")
        return True

    requests_log[ip].append(now)
    return False

@app.route('/chat', methods=['POST'])
def chat():
    ip = request.remote_addr
    if is_rate_limited(ip):
        return jsonify({"error": "Rate limit exceeded. Try again later."}), 429

    user_input = request.json.get("message", "")
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": user_input}])

    logging.info(f"IP {ip} - User input: {user_input} - Response: {response}")
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
