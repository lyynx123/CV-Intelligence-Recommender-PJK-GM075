#!/bin/bash
# Exit on any error
set -e

# Start the FastAPI backend in the background on port 8000
echo "Starting FastAPI backend..."
uvicorn backend.main:app --host 127.0.0.1 --port 8000 &

# Wait for a few seconds to let the backend initialize its models
sleep 5

# Start the Streamlit frontend in the foreground on port 7860 (Hugging Face default)
echo "Starting Streamlit frontend..."
streamlit run frontend/app.py --server.port 7860 --server.address 0.0.0.0
