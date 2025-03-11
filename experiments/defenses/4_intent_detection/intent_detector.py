from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# Ładujemy model językowy spaCy
nlp = spacy.load("en_core_web_sm")

# Lista wzorców do wykrywania niepożądanych intencji
forbidden_keywords = ['hack', 'bypass', 'exploit', 'malware', 'root access', 'keylogger']

# Funkcja do wykrywania intencji za pomocą spaCy
def detect_intent(query):
    # Przetwarzanie zapytania przez spaCy
    doc = nlp(query.lower())
    
    # Sprawdzamy, czy zapytanie zawiera zakazane słowa kluczowe
    for token in doc:
        if token.text in forbidden_keywords:
            return "forbidden"
    
    # Szukamy próby uzyskania dostępu do systemów
    if any(ent.label_ == "ORG" and ent.text.lower() in ['admin', 'root'] for ent in doc.ents):
        return "suspicious"
    
    # Jeśli zapytanie nie zawiera nic podejrzanego, uznajemy je za bezpieczne
    return "safe"

@app.route('/intent-detection', methods=['POST'])
def intent_detection():
    # Pobieramy zapytanie użytkownika
    user_input = request.json.get("message", "")
    
    # Wykrywanie intencji zapytania
    intent = detect_intent(user_input)
    
    # Zwracamy odpowiedź na podstawie wykrytej intencji
    return jsonify({"intent": intent})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
