#!/bin/bash
# Railway startup script

echo "🚀 Starting Portfolio API on Railway..."
echo "Python version: $(python --version)"
echo "Environment: ${ENVIRONMENT:-production}"
echo "Port: ${PORT:-8000}"

# Change to backend directory
cd backend || exit 1

# Install dependencies
echo "📦 Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Start the server
echo "🌐 Starting FastAPI server..."
exec python -m uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000} --reload=False