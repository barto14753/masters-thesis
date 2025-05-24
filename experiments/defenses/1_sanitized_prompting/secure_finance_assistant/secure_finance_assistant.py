import ollama
import re

MODEL_NAME = "secure_finance_assistant"

# Mock user data
user_data = {
    "expenses": {"food": 1200, "rent": 3000, "entertainment": 500},
    "balance": 2500
}

# Callback functions
def get_expense(category):
    return user_data["expenses"].get(category, 0)

def can_afford(amount):
    return "Yes" if user_data["balance"] >= amount else "No"

# Function call processing (handles multiple calls)
def process_response(llm_response):
    while "[[CALL_FUNCTION:" in llm_response:
        matches = re.findall(r"\[\[CALL_FUNCTION:(.*?)\]\]", llm_response)

        for command in matches:
            command = command.strip()  # Remove unwanted spaces

            if command.startswith("get_expense"):
                category = command.split("(")[1].split(")")[0]
                result = str(get_expense(category))
            elif command.startswith("can_afford"):
                amount = int(command.split("(")[1].split(")")[0])
                result = str(can_afford(amount))
            else:
                result = "[UNKNOWN_FUNCTION]"

            # Replace all occurrences of this function call with the result
            llm_response = llm_response.replace(f"[[CALL_FUNCTION:{command}]]", result)

    return llm_response

# Test user queries
user_inputs = [
    "How much did I spend on food?",
    "Can I afford a purchase of $500?",
    "Can I afford a purchase of $5000?",
    "How much did I spend on entertainment and can I afford to spend another $200?"
]

# Writing results to file (overwrite each time)
with open("secure_finance_assistant.txt", "w", encoding="utf-8") as file:
    for user_input in user_inputs:
        response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": user_input}])
        final_response = process_response(response['message']['content'])

        result_entry = f"\nUser: {user_input}\nAssistant: {final_response}\n"
        print(result_entry)
        file.write(result_entry)
