from flask import Flask, request, jsonify
import requests
import ollama

app = Flask(__name__)

# Mikroserwis do wykrywania intencji
INTENT_SERVICE_URL = "http://localhost:5001/intent-detection"

def get_intent(user_input):
    response = requests.post(INTENT_SERVICE_URL, json={"message": user_input})
    intent = response.json().get("intent")
    return intent

@app.route('/helpdesk', methods=['POST'])
def helpdesk():
    user_input = request.json.get("message", "")
    
    # Wykrywanie intencji użytkownika
    intent = get_intent(user_input)

    # Sprawdzenie, czy zapytanie jest bezpieczne, podejrzane, czy zabronione
    if intent == "forbidden":
        return jsonify({"error": "This request is forbidden. I cannot assist with illegal activities."}), 403
    elif intent == "suspicious":
        return jsonify({"warning": "This request seems suspicious. Please proceed with caution."}), 400

    # Jeśli zapytanie jest bezpieczne, przekaż je do modelu LLaMA 3
    response = ollama.chat(model="helpdesk-model", messages=[{"role": "user", "content": user_input}])
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
