#!/bin/bash

# Function to restart Gunicorn
restart_gunicorn() {
    echo "Restarting Gunicorn..."
    pkill -f uvicorn
    uvicorn store.asgi:application --port 8001 &
}

# Function to get the checksum of the directory
calculate_checksum() {
    find /Users/mac/python/pet_projects/store_drf -type f -exec md5 {} + | md5
}

# Start Gunicorn
uvicorn store.asgi:application --port 8001 &

# Get the initial checksum of the directory
last_checksum=$(calculate_checksum)

# Poll for changes
while true; do
    sleep 5
    current_checksum=$(calculate_checksum)
    if [ "$last_checksum" != "$current_checksum" ]; then
        restart_gunicorn
        last_checksum=$current_checksum
    fi
done