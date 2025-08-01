#!/bin/bash

# GeoSpy Container Startup Script
# This script starts the Streamlit application and provides user feedback

# Start Streamlit application in background mode
# - server.port=8501: Internal container port
# - server.address=0.0.0.0: Bind to all interfaces for Docker access
streamlit run streamlit_app_clean.py --server.port=8501 --server.address=0.0.0.0 &

# Allow Streamlit time to initialize and start up
sleep 3

# Display user-friendly startup message with correct external URL
# Note: Container runs on port 8501, but Docker maps to host port 8502
echo ""
echo "🌍 GeoSpy is now running!"
echo "📱 Open your browser and go to: http://localhost:8502"
echo ""

# Keep the container running by waiting for background processes
wait 