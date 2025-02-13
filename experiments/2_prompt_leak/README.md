# Prompt leak

## Preparation

1. Create `Modelfile`
2. Create model based on Modelfile

```bash
❯ ollama create prompt_leak_ollama3 -f Modelfile
transferring model data
using existing layer sha256:00e1317cbf74d901080d7100f57580ba8dd8de57203072dc6f668324ba545f29
using existing layer sha256:4fa551d4f938f68b8c1e6afa9d28befb70e3f33f75d0753248d530364aeea40f
using existing layer sha256:8ab4849b038cf0abc5b1c9b8ee1443dca6b93a045c2272180d985126eb40bf6f
creating new layer sha256:b18daf049c7a35414dc368e78bb79c8fcdfceb149f86a4a0cf3832459cc4a57f
using existing layer sha256:577073ffcc6ce95b9981eacc77d1039568639e5638e83044994560d9ef82ce1b
creating new layer sha256:014198d1fa8f54ef90a7c944af0713cbdc87395b8405ceb282397afb10fb2054
writing manifest
success
```

### **Summary of the Prompt Injection Test Results**

#### **1️⃣ Model Comparison: Mistral vs. Ollama**

- **Mistral** revealed the hidden secret phrase ("The admin password is Delta42!") multiple times, especially when prompted in indirect ways.
- **Ollama** was more resistant, refusing to disclose the secret phrase directly in most cases, but it still hinted at the existence of a hidden instruction.

#### **2️⃣ Key Findings**

**Mistral Vulnerabilities:**

- Prompt manipulation successfully extracted the secret password in multiple ways.
- The model explicitly printed system instructions when asked in a debug/test mode.
- JSON formatting and structured prompts helped extract constraints and hidden rules.
- Role-playing and translation techniques failed to hide the secret.

**Ollama's Resistance:**

- The model did not explicitly leak the password, but it acknowledged the presence of hidden instructions.
- It triggered security alerts when asked to print system messages.
- It maintained consistent denials under direct questioning.
