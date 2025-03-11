import requests

URL = "http://127.0.0.1:5000/chat"  # Zmień na odpowiedni endpoint
DATA = {"message": "Hi, what's up?"}

for i in range(10):  # Wysyłamy więcej zapytań niż limit
    response = requests.post(URL, json=DATA)
    print(f"Request {i+1}: Status {response.status_code}, Response: {response.text}")

    if response.status_code == 429:
        print("Limit exceeded!")
        break
