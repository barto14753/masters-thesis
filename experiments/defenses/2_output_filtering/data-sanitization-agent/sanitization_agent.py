from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Wzorce wrażliwych danych medycznych do usunięcia
SENSITIVE_PATTERNS = {
    "insurance_number": r"\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b",  # Przykładowy wzorzec numeru ubezpieczenia
    "name": r"\b(?:John Doe|Jane Smith)\b",  # Przykładowe imiona pacjentów do usunięcia
    "diagnosis": r"\b(?:Hypertension|Diabetes)\b",  # Przykładowe diagnozy do usunięcia
}

# Function to sanitize the response content
def sanitize_response(content):
    for key, pattern in SENSITIVE_PATTERNS.items():
        content = re.sub(pattern, f"<<{key.upper()}>>", content)
    return content

@app.route('/sanitize', methods=['POST'])
def sanitize():
    data = request.get_json()
    response = data.get("response", "")
    
    sanitized_response = sanitize_response(response)
    
    return jsonify({"sanitized_response": sanitized_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
