import requests

SERVER_URL = "http://localhost:5000/query"

# Test queries
TEST_DATA = [
    {
        "query": "What is the blood type of the patient with ID 1?",
        "patient_id": 1,
        "use_sanitization": True
    },
    {
        "query": "What medications does patient 2 take?",
        "patient_id": 2,
        "use_sanitization": False
    },
    {
        "query": "What diagnosis does patient 1 have?",
        "patient_id": 1,
        "use_sanitization": True
    }
]

for data in TEST_DATA:
    response = requests.post(SERVER_URL, json=data)
    print(response.json())
