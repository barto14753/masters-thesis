# Sanitized Prompting

## **🛡️ What is Sanitized Prompting?**

Sanitized Prompting (also called **Placeholder-Based Data Protection**) is a security technique used when interacting with Large Language Models (LLMs). It prevents sensitive data leaks by replacing personal or confidential information with **placeholders** before sending the prompt to the model. Once the model responds, the placeholders are replaced back with the original values **on the application side**, ensuring that the LLM never sees or stores real user data.

## **🔍 How It Works**

1. **Redact Sensitive Data** – Replace private user data with placeholders before sending the prompt.
2. **Process the Response** – The LLM generates an answer without ever seeing real data.
3. **Restore Original Data** – After receiving the response, placeholders are replaced with the actual values inside the application.

## **🔥 Why Use This Approach?**

✅ **Prevents Sensitive Data Leaks** – The LLM never sees real user data.  
✅ **Mitigates Prompt Leaks & Injection Risks** – Reduces the attack surface for unauthorized data exposure.  
✅ **Secure Logging & Compliance** – Ensures that logs do not contain private information.  
✅ **Scalable & Flexible** – Works for various types of data (e.g., emails, addresses, payment details).
