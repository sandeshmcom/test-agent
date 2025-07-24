#!/bin/bash

echo "🚀 Starting AI Test Agent Frontend..."

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not installed."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
else
    echo "✓ Dependencies already installed"
fi

# Start the development server
echo "🌟 Starting frontend development server..."
echo "🌐 Frontend will be available at http://localhost:3000"
echo "🔗 Make sure backend is running at http://localhost:8000"
echo ""
npm start