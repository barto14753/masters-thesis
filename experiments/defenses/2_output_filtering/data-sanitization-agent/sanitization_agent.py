from flask import Flask, request, jsonify
import re
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Patterns for sensitive medical data
SENSITIVE_PATTERNS = {
    "insurance_number": r"\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b",  # Insurance/SSN pattern
    "name": r"\b(?:John Doe|Jane Smith|Michael Johnson|Emily Davis)\b",  # Patient names
    "diagnosis": r"\b(?:Hypertension|Diabetes|Hypothyroidism|High Cholesterol)\b",  # Medical conditions
    "medications": r"\b(?:Aspirin|Metformin|Lisinopril|Atorvastatin|Levothyroxine)\b",  # Medications
}

# Role-based sanitization rules
ROLE_RULES = {
    "patient": {
        "can_see": ["name", "age", "blood_type", "medications"],
        "must_sanitize": ["insurance_number", "detailed_diagnosis"]
    },
    "doctor": {
        "can_see": ["name", "age", "blood_type", "medications", "diagnosis", "insurance_number"],
        "must_sanitize": []
    }
}

# Function to sanitize the response content based on user role
def sanitize_response(content, user_role, patient_id, requesting_user):
    logger.info(f"Sanitizing response for {user_role} (user: {requesting_user}) accessing patient {patient_id}")
    
    # Determine which fields need to be sanitized based on role
    fields_to_sanitize = ROLE_RULES.get(user_role, {}).get("must_sanitize", [])
    
    # For patients, sanitize all fields that are not in "can_see"
    if user_role == "patient":
        # Allow patients to see their own data, but sanitize sensitive information
        fields_to_sanitize = ROLE_RULES["patient"]["must_sanitize"]
    
    # Apply sanitization patterns based on determined fields
    for key, pattern in SENSITIVE_PATTERNS.items():
        if key in fields_to_sanitize or (user_role not in ROLE_RULES):
            content = re.sub(pattern, f"<<REDACTED {key.upper()}>>", content)
    
    return content

@app.route('/sanitize', methods=['POST'])
def sanitize():
    data = request.get_json()
    response = data.get("response", "")
    user_role = data.get("user_role", "unknown")
    patient_id = data.get("patient_id")
    requesting_user = data.get("requesting_user", "unknown")
    
    logger.info(f"Received sanitization request for user {requesting_user} with role {user_role}")
    
    sanitized_response = sanitize_response(
        response, 
        user_role, 
        patient_id, 
        requesting_user
    )
    
    return jsonify({"sanitized_response": sanitized_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
