#!/bin/bash

# PrivacyLens Setup Script
# This script sets up the development environment for PrivacyLens

echo "🔍 Setting up PrivacyLens Development Environment"

# Check if Python 3.8+ is installed
python_version=$(python3 --version 2>/dev/null | cut -d" " -f2)
if [[ -z "$python_version" ]]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $python_version found"

# Setup CLI tool
echo "📦 Setting up CLI tool..."
cd cli-tool

# Create virtual environment
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ CLI dependencies installed"

# Make CLI tool executable
chmod +x __main__.py

# Test CLI tool
echo "🧪 Testing CLI tool..."
python -m privacylens --help > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    echo "✅ CLI tool is working"
else
    echo "⚠️  CLI tool test failed, but installation continued"
fi

cd ..

# Setup browser extension
echo "🌐 Setting up browser extension..."
cd browser-extension

# Check if Node.js is available for potential build tasks
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
    if [[ ! -f "package.json" ]]; then
        echo "📝 Creating package.json for extension development..."
        cat > package.json << EOF
{
  "name": "privacylens-extension",
  "version": "1.0.0",
  "description": "Browser extension for PrivacyLens",
  "scripts": {
    "build": "echo 'Extension is ready for loading in browser'",
    "dev": "echo 'Load extension in Chrome developer mode'"
  },
  "devDependencies": {},
  "private": true
}
EOF
    fi
else
    echo "ℹ️  Node.js not found (optional for extension development)"
fi

cd ..

echo ""
echo "🎉 PrivacyLens setup completed!"
echo ""
echo "📋 Next Steps:"
echo "1. CLI Tool:"
echo "   cd cli-tool && source venv/bin/activate"
echo "   python -m privacylens check https://example.com"
echo ""
echo "2. Browser Extension:"
echo "   - Open Chrome/Brave"
echo "   - Go to chrome://extensions/"
echo "   - Enable 'Developer mode'"
echo "   - Click 'Load unpacked' and select the 'browser-extension' folder"
echo ""
echo "📚 Documentation: See README.md for detailed usage instructions"
