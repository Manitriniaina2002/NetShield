#!/bin/bash
# Production startup script for Render deployment

# Exit on error
set -e

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations/setup if needed
echo "Application ready for deployment"

# Start Uvicorn
echo "Starting application..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
