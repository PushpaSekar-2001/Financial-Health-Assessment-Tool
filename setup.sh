#!/bin/bash
# Financial Health Assessment Tool - Setup Script
# This script automates the installation and setup process

echo "=========================================="
echo "Financial Health Assessment Tool Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python detected: $(python3 --version)"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

echo "✅ Node.js detected: $(node --version)"

# Backend Setup
echo ""
echo "=========================================="
echo "Setting up Backend..."
echo "=========================================="

cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend setup complete!"
echo ""

# Frontend Setup
echo "=========================================="
echo "Setting up Frontend..."
echo "=========================================="

cd ../frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete!"
echo ""

# Summary
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   python app.py"
echo ""
echo "2. Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "Backend API: http://127.0.0.1:5000"
echo "Frontend: http://localhost:3000"
echo ""
