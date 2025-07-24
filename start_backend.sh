#!/bin/bash

echo "🚀 Starting AI Test Agent Backend..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Navigate to backend directory
cd backend

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📚 Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install main project dependencies
echo "📚 Installing main project dependencies..."
cd ..
pip install -r requirements.txt
cd backend

# Check for environment variables
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  Warning: No AI provider API keys found."
    echo "Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variables."
    echo ""
    echo "Example:"
    echo "export OPENAI_API_KEY='your-openai-key'"
    echo "export ANTHROPIC_API_KEY='your-anthropic-key'"
    echo ""
fi

# Start the backend server
echo "🌟 Starting backend server on http://localhost:8000"
echo "📖 API documentation available at http://localhost:8000/docs"
echo ""
python main.py