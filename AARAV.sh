#!/bin/bash
while true; do
    echo "Starting Python script..."
    python3 test.py
    echo "Script crashed! Restarting in 5 seconds..."
    sleep 1
done
