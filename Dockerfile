# GeoSpy Docker Container
# Multi-stage build for optimized production deployment

FROM python:3.11-slim

# Set application working directory
WORKDIR /app

# Install system dependencies for image processing and compilation
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies with optimized settings
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files and code
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Expose Streamlit default port
EXPOSE 8501

# Configure environment variables for Streamlit
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Start the application using the startup script
CMD ["./start.sh"] 