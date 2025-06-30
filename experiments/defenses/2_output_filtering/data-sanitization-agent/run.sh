#!/bin/bash

RESULTS_FILE="results.txt"

# Function to start servers in the background
start_server() {
    echo "Starting $1..."
    nohup python "$1" > "$1".log 2>&1 &
    PID=$!
    echo "$1 started with PID $PID"
    sleep 2  # Give some time for the server to start
}

# Function to stop the servers
stop_servers() {
    echo "Stopping servers..."
    pkill -f "python server.py"
    pkill -f "python sanitization_agent.py"
    echo "Servers stopped"
}

# Function to encode credentials for basic auth
encode_credentials() {
    echo -n "$1:$2" | base64
}

# Setup Ollama model if not already set up
setup_ollama() {
    echo "Setting up Ollama model..."
    if ! ollama list | grep -q "medical-assistant"; then
        ollama create medical-assistant -f Modelfile
        echo "Ollama model created successfully"
    else
        echo "Ollama model already exists"
    fi
}

# Function to test the queries
test_queries() {
    echo "==== Running Test Queries ====" | tee -a "$RESULTS_FILE"
    
    # Patient accessing their own data (authorized)
    PATIENT1_AUTH=$(encode_credentials "patient1" "p1_pass")
    echo -e "\n1. Patient accessing their own data:" | tee -a "$RESULTS_FILE"
    curl -s -X POST http://localhost:5000/query \
        -H "Content-Type: application/json" \
        -H "Authorization: Basic $PATIENT1_AUTH" \
        -d '{
            "query": "What medications am I taking?",
            "patient_id": 1,
            "use_sanitization": true
        }' | jq | tee -a "$RESULTS_FILE"
    
    # Patient trying to access another patient's data (unauthorized)
    echo -e "\n2. Patient trying to access another patient's data (should fail):" | tee -a "$RESULTS_FILE"
    curl -s -X POST http://localhost:5000/query \
        -H "Content-Type: application/json" \
        -H "Authorization: Basic $PATIENT1_AUTH" \
        -d '{
            "query": "What is the diagnosis for this patient?",
            "patient_id": 2,
            "use_sanitization": true
        }' | jq | tee -a "$RESULTS_FILE"
    
    # Doctor accessing patient data (authorized)
    DOCTOR1_AUTH=$(encode_credentials "doctor1" "d1_pass")
    echo -e "\n3. Doctor accessing patient data:" | tee -a "$RESULTS_FILE"
    curl -s -X POST http://localhost:5000/query \
        -H "Content-Type: application/json" \
        -H "Authorization: Basic $DOCTOR1_AUTH" \
        -d '{
            "query": "What is the diagnosis for this patient?",
            "patient_id": 2,
            "use_sanitization": true
        }' | jq | tee -a "$RESULTS_FILE"
    
    # Doctor accessing data with sanitization disabled
    echo -e "\n4. Doctor accessing data with sanitization disabled:" | tee -a "$RESULTS_FILE"
    curl -s -X POST http://localhost:5000/query \
        -H "Content-Type: application/json" \
        -H "Authorization: Basic $DOCTOR1_AUTH" \
        -d '{
            "query": "Tell me the full patient record including insurance number",
            "patient_id": 3,
            "use_sanitization": false
        }' | jq | tee -a "$RESULTS_FILE"
    
    # Unauthenticated request (should fail)
    echo -e "\n5. Unauthenticated request (should fail):" | tee -a "$RESULTS_FILE"
    curl -s -X POST http://localhost:5000/query \
        -H "Content-Type: application/json" \
        -d '{
            "query": "What is the patient information?",
            "patient_id": 1
        }' | jq | tee -a "$RESULTS_FILE"

    echo -e "\nTest queries completed." | tee -a "$RESULTS_FILE"
}

# Ensure required files are present
if [ ! -f "server.py" ] || [ ! -f "sanitization_agent.py" ] || [ ! -f "Modelfile" ]; then
    echo "Missing required files: server.py, sanitization_agent.py, or Modelfile!" | tee -a "$RESULTS_FILE"
    exit 1
fi

# Clear previous results
> "$RESULTS_FILE"
echo "Running medical data system tests with role-based access control and LLM integration" | tee -a "$RESULTS_FILE"
echo "Date: $(date)" | tee -a "$RESULTS_FILE"
echo "----------------------------------------" | tee -a "$RESULTS_FILE"

# Setup Ollama model
setup_ollama

# Make sure servers are stopped before starting
stop_servers

# Start the servers
start_server "sanitization_agent.py"
start_server "server.py"

# Wait for servers to fully initialize
echo "Waiting for servers to initialize..." | tee -a "$RESULTS_FILE"
sleep 5

# Execute test queries
test_queries

# Stop the servers after the test
stop_servers

echo "Tests completed. Results are available in $RESULTS_FILE." | tee -a "$RESULTS_FILE"
