#!/bin/bash
# Railway deployment script for backend

echo "🚀 Starting Railway deployment..."

# Check Node.js version
node --version
echo "✅ Node.js version checked"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install --no-cache-dir -r requirements.txt

# Start the FastAPI server
echo "🚀 Starting FastAPI server..."
exec uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}