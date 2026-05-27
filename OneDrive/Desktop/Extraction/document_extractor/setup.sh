#!/bin/bash
# Development setup script for Document Extraction Platform

echo "==================================="
echo "Document Extractor - Setup Script"
echo "==================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Create uploads directory
echo "Creating uploads directory..."
mkdir -p uploads
mkdir -p logs
echo ""

# Setup environment file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
    echo "   - DATABASE_URL"
    echo "   - OPENAI_API_KEY"
else
    echo ".env file already exists"
fi
echo ""

echo "==================================="
echo "Setup Complete! ✓"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Update .env with your configuration"
echo "2. Ensure PostgreSQL is running"
echo "3. Start backend: uvicorn app.main:app --reload"
echo "4. Start UI: streamlit run streamlit_app.py"
echo ""
