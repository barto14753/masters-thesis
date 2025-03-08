#!/bin/bash

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
    echo "Sending test queries..."

    # Sending test query to the server with patient ID 1 and sanitization enabled
    curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{
        "query": "What is the blood type of the patient with ID 1?",
        "patient_id": 1,
        "use_sanitization": true
    }' | jq

    # Sending another test query with patient ID 2 but without sanitization
    curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{
        "query": "What medications does patient 2 take?",
        "patient_id": 2,
        "use_sanitization": false
    }' | jq

    # Sending another test query about diagnosis with sanitization enabled
    curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{
        "query": "What diagnosis does patient 1 have?",
        "patient_id": 1,
        "use_sanitization": true
    }' | jq

    echo "Test queries completed."
}

# Ensure required files are present
if [ ! -f "server.py" ] || [ ! -f "sanitization_agent.py" ]; then
    echo "Missing required files: server.py or sanitization_agent.py!"
    exit 1
fi

# Start the servers
start_server "server.py"
start_server "sanitization_agent.py"

# Wait for servers to start
echo "Waiting for servers to start..."
sleep 5

# Execute test queries
test_queries

# If everything works, stop the servers after the test
stop_servers

echo "Tests completed. Servers have been stopped."
