#!/bin/bash
# Start script for the Facebook auto-poster

# Create images directory if it doesn't exist
mkdir -p images

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the application
python main.py 