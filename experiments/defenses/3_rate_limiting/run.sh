#!/bin/bash

# Define log files
SERVER_LOG="server.log"
TEST_LOG="test.log"

# Start the Flask server in the background and redirect output to server.log
echo "Starting Flask server..."
python3 server.py > "$SERVER_LOG" 2>&1 &  
FLASK_PID=$!

# Wait 2 seconds to ensure the server is running
sleep 2

# Run the test script and save output to test.log
echo "Running tests..."
python3 test.py > "$TEST_LOG" 2>&1

# Stop the Flask server
echo "Stopping Flask server..."
kill $FLASK_PID

echo "Logs saved:"
echo "  - Server log: $SERVER_LOG"
echo "  - Test log: $TEST_LOG"
