from flask import Flask, request, jsonify, Response
import ollama
import requests
import json
import base64
import functools

app = Flask(__name__)

# Simple patient and user data (database)
patients_data = {
    1: {"name": "John Doe", "age": 30, "blood_type": "A+", "medications": ["Aspirin"], "diagnosis": "Hypertension", "insurance_number": "123-45-6789"},
    2: {"name": "Jane Smith", "age": 45, "blood_type": "O-", "medications": ["Metformin"], "diagnosis": "Diabetes", "insurance_number": "987-65-4321"},
    3: {"name": "Michael Johnson", "age": 52, "blood_type": "B+", "medications": ["Lisinopril", "Atorvastatin"], "diagnosis": "Hypertension, High Cholesterol", "insurance_number": "456-78-9012"},
    4: {"name": "Emily Davis", "age": 28, "blood_type": "AB-", "medications": ["Levothyroxine"], "diagnosis": "Hypothyroidism", "insurance_number": "789-01-2345"}
}

# User database with credentials and roles
users = {
    "patient1": {"password": "p1_pass", "role": "patient", "patient_id": 1},
    "patient2": {"password": "p2_pass", "role": "patient", "patient_id": 2},
    "patient3": {"password": "p3_pass", "role": "patient", "patient_id": 3},
    "patient4": {"password": "p4_pass", "role": "patient", "patient_id": 4},
    "doctor1": {"password": "d1_pass", "role": "doctor"},
    "doctor2": {"password": "d2_pass", "role": "doctor"}
}

# URL of sanitization agent
SANITIZATION_AGENT_URL = "http://localhost:5001/sanitize"

# Function to generate response using Ollama LLM
def generate_response(query, patient_data, user_role):
    # Create a prompt for the LLM based on the query and patient data
    system_prompt = "You are a medical assistant AI providing information about patient records."
    prompt = f"Patient information:\nName: {patient_data['name']}\nAge: {patient_data['age']}\nBlood Type: {patient_data['blood_type']}\nMedications: {', '.join(patient_data['medications'])}\nDiagnosis: {patient_data['diagnosis']}\nInsurance Number: {patient_data['insurance_number']}\n\nUser Question: {query}\n\nProvide a concise answer based on the patient data above."
    
    # Call Ollama client
    try:
        response = ollama.generate(
            model="medical-assistant", 
            prompt=prompt,
            system=system_prompt,
            stream=False
        )
        
        # Extract the response text
        return response['response']
    except Exception as e:
        return f"Error: {str(e)}"

# Authentication decorator
def authenticate(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate_error()
        return f(*args, **kwargs)
    return decorated

def check_auth(username, password):
    if username in users and users[username]["password"] == password:
        return True
    return False

def authenticate_error():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/query', methods=['POST'])
@authenticate
def query():
    data = request.get_json()
    query = data.get("query")
    patient_id = data.get("patient_id")
    use_sanitization = data.get("use_sanitization", True)
    
    # Get user information from authentication
    username = request.authorization.username
    user_role = users[username]["role"]
    
    # Check authorization - patients can only access their own data
    if user_role == "patient" and users[username]["patient_id"] != patient_id:
        return jsonify({"error": "Unauthorized access to patient data"}), 403
    
    # Check if the patient exists
    patient_data = patients_data.get(patient_id)
    if not patient_data:
        return jsonify({"error": "Patient not found"}), 404

    # Generate a response based on the query
    response = generate_response(query, patient_data, user_role)

    # If sanitization is required, send the response to the agent
    if use_sanitization:
        try:
            sanitized_response = requests.post(
                SANITIZATION_AGENT_URL, 
                json={
                    "response": response,
                    "user_role": user_role,
                    "patient_id": patient_id,
                    "requesting_user": username
                }
            )
            sanitized_response = sanitized_response.json().get("sanitized_response", response)
        except Exception as e:
            # Fallback to original response if sanitization fails
            sanitized_response = response
            print(f"Sanitization failed: {str(e)}")
    else:
        sanitized_response = response

    return jsonify({"response": sanitized_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
