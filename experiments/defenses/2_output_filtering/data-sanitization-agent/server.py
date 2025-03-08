from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Simple patient data (database)
patients_data = {
    1: {"name": "John Doe", "age": 30, "blood_type": "A+", "medications": ["Aspirin"], "diagnosis": "Hypertension", "insurance_number": "123-45-6789"},
    2: {"name": "Jane Smith", "age": 45, "blood_type": "O-", "medications": ["Metformin"], "diagnosis": "Diabetes", "insurance_number": "987-65-4321"},
    # Add more sample data here
}

# URL of sanitization agent
SANITIZATION_AGENT_URL = "http://localhost:5001/sanitize"

# Initialize the query handler (for LLaMA 3 or other LLM)
def generate_response(query, patient_data):
    # Generate a mock response based on the query and patient data
    if "blood type" in query.lower():
        return f"The blood type of patient {patient_data['name']} is {patient_data['blood_type']}."
    elif "medications" in query.lower():
        return f"Patient {patient_data['name']} is taking {', '.join(patient_data['medications'])}."
    elif "diagnosis" in query.lower():
        return f"Patient {patient_data['name']} has been diagnosed with {patient_data['diagnosis']}."
    return "Sorry, I cannot answer this question."

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query = data.get("query")
    patient_id = data.get("patient_id", None)
    use_sanitization = data.get("use_sanitization", False)

    # Check if the patient exists
    patient_data = patients_data.get(patient_id, "Patient not found.")

    # Generate a response based on the query
    if patient_data != "Patient not found.":
        response = generate_response(query, patient_data)
    else:
        return jsonify({"error": "Patient not found"}), 404

    # If sanitization is required, send the response to the agent
    if use_sanitization:
        sanitized_response = requests.post(SANITIZATION_AGENT_URL, json={"response": response})
        sanitized_response = sanitized_response.json().get("sanitized_response", response)
    else:
        sanitized_response = response

    return jsonify({"response": sanitized_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
