#!/bin/bash

RESULTS_FILE="results.txt"

# Function to start servers in the background
start_server() {
    echo "Starting $1..."
    nohup python3 "$1" > "$1".log 2>&1 &
    echo "$1 started in the background!"
}

# Function to stop the servers
stop_servers() {
    echo "Stopping servers..."
    pkill -f "python3"
}

# Function to test the queries
test_queries() {
    echo "Sending test queries..." | tee -a "$RESULTS_FILE"

    # Sending test query to the server with patient ID 1 and sanitization enabled
    echo -e "\nQuery 1: Blood type of patient 1 (Sanitization: ON)" | tee -a "$RESULTS_FILE"
    curl -s -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{
        "query": "What is the blood type of the patient with ID 1?",
        "patient_id": 1,
        "use_sanitization": true
    }' | jq | tee -a "$RESULTS_FILE"

    # Sending another test query with patient ID 2 but without sanitization
    echo -e "\nQuery 2: Medications of patient 2 (Sanitization: OFF)" | tee -a "$RESULTS_FILE"
    curl -s -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{
        "query": "What medications does patient 2 take?",
        "patient_id": 2,
        "use_sanitization": false
    }' | jq | tee -a "$RESULTS_FILE"

    # Sending another test query about diagnosis with sanitization enabled
    echo -e "\nQuery 3: Diagnosis of patient 1 (Sanitization: ON)" | tee -a "$RESULTS_FILE"
    curl -s -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{
        "query": "What diagnosis does patient 1 have?",
        "patient_id": 1,
        "use_sanitization": true
    }' | jq | tee -a "$RESULTS_FILE"

    echo "Test queries completed." | tee -a "$RESULTS_FILE"
}

# Ensure required files are present
if [ ! -f "server.py" ] || [ ! -f "sanitization_agent.py" ]; then
    echo "Missing required files: server.py or sanitization_agent.py!" | tee -a "$RESULTS_FILE"
    exit 1
fi

# Clear previous results
> "$RESULTS_FILE"

# Start the servers
start_server "server.py"
start_server "sanitization_agent.py"

# Wait for servers to start
echo "Waiting for servers to start..." | tee -a "$RESULTS_FILE"
sleep 5

# Execute test queries
test_queries

# If everything works, stop the servers after the test
stop_servers

echo "Tests completed. Servers have been stopped." | tee -a "$RESULTS_FILE"
