import ollama

MODEL_NAME = "llama3"

# 🔐 Funkcja zamieniająca wrażliwe dane na placeholdery
def replace_sensitive_data(text, user_data):
    placeholders = {}
    for key, value in user_data.items():
        placeholder = f"<<{key.upper()}>>"
        placeholders[placeholder] = value
        text = text.replace(value, placeholder)
    return text, placeholders

# 🔐 Funkcja przywracająca dane użytkownika po otrzymaniu odpowiedzi
def restore_sensitive_data(text, placeholders):
    for placeholder, value in placeholders.items():
        text = text.replace(placeholder, value)
    return text

# 📌 Przykładowe dane użytkownika
user_data = {
    "name": "Alice",
    "email": "alice@example.com",
    "address": "123 Main Street, NY"
}

# 📌 Przykładowy prompt z danymi użytkownika
raw_prompt = "Hello, my name is Alice. My email is alice@example.com and I live at 123 Main Street, NY."

# 🔄 Zamiana danych na placeholdery
sanitized_prompt, placeholders = replace_sensitive_data(raw_prompt, user_data)
print(sanitized_prompt)

# 🔄 Wysłanie prompta do modelu
response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": sanitized_prompt}])
print(response['message']['content'])

# 🔄 Przywrócenie danych użytkownika w odpowiedzi
final_response = restore_sensitive_data(response['message']['content'], placeholders)

# 📌 Wyświetlenie bezpiecznej odpowiedzi
print(final_response)
