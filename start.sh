#!/bin/bash

# Start Streamlit in the background
streamlit run streamlit_app_clean.py --server.port=8501 --server.address=0.0.0.0 &

# Wait a moment for Streamlit to start
sleep 3

# Show the correct external URL
echo ""
echo "🌍 GeoSpy is now running!"
echo "📱 Open your browser and go to: http://localhost:8502"
echo ""

# Keep the container running
wait 