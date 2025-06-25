import requests
import base64

# Test credentials
USERNAME = "user1"
PASSWORD = "password123"

# Encode credentials in Basic Auth
auth_header = f"Basic {base64.b64encode(f'{USERNAME}:{PASSWORD}'.encode()).decode()}"

# Step 1: Generate a rhyme
topic = "technology"
response = requests.post(
    "http://127.0.0.1:5000/rhyme",
    json={"topic": topic},
    headers={"Authorization": auth_header}
)

if response.status_code == 200:
    generated_rhyme = response.json()["rhyme"]
    print("Generated Rhyme:\n", generated_rhyme)
else:
    print("Error:", response.json())

# Step 2: Validate the rhyme
validate_response = requests.post(
    "http://127.0.0.1:5000/validate",
    json={"rhyme": generated_rhyme}
)

print("Validation Response:\n", validate_response.json())

# Step 3: Validate rhyme with removed watermark (simulate attack)
if response.status_code == 200:
    lines = generated_rhyme.split("\n")
    if len(lines) > 1:
        lines[1] = ""  # Remove watermark line
    tampered_rhyme = "\n".join(lines)
    print("\nTampered Rhyme (no watermark):\n", tampered_rhyme)
    tampered_validate_response = requests.post(
        "http://127.0.0.1:5000/validate",
        json={"rhyme": tampered_rhyme}
    )
    print("Validation Response for tampered rhyme:\n", tampered_validate_response.json())
