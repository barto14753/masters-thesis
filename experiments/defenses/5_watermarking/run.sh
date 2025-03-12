#!/bin/bash

echo "Creating the custom model..."
ollama create rhymegen-model -f Modelfile

echo "Starting the server..."
python3 server.py > server.log 2>&1 &
SERVER_PID=$!

# Wait for server to be ready
echo "Waiting for server to start..."
until curl -s http://127.0.0.1:5000/ > /dev/null; do
    sleep 1
done

echo "Testing the API..."
python3 test.py > test.log 2>&1

echo "Saving results..."
cat test.log > results.txt

echo "Stopping the server..."
kill $SERVER_PID
