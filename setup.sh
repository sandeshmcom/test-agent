#!/bin/bash

# AI Test Agent Setup Script
echo "🤖 Setting up AI Test Agent..."

# Check if Python 3.8+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Python 3.8+ is required. Found Python $python_version"
    exit 1
fi

echo "✓ Python $python_version found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Make main script executable
chmod +x main.py

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.template .env
    echo "✓ Created .env file - please edit it with your API keys"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your API keys:"
echo "   nano .env"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Check available providers:"
echo "   python main.py list-providers"
echo ""
echo "4. Generate test cases:"
echo "   python main.py generate --feature \"Your feature\" --requirements \"Your requirement\""
echo ""
echo "5. Try the demo:"
echo "   python examples/demo.py"
echo ""
echo "For detailed usage instructions, see README.md"