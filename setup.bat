#!/bin/bash
# Windows Setup Script for Financial Health Assessment Tool
# Run this in PowerShell as Administrator

echo "=========================================="
echo "Financial Health Assessment Tool - Setup"
echo "=========================================="
echo ""

# Check Python
echo "Checking Python installation..."
python --version

# Check Node
echo "Checking Node.js installation..."
node --version

# Backend Setup
echo ""
echo "=========================================="
echo "Setting up Backend..."
echo "=========================================="
echo ""

cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
call venv\Scripts\activate.bat

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Backend setup complete!"
echo ""

# Frontend Setup
echo "=========================================="
echo "Setting up Frontend..."
echo "=========================================="
echo ""

cd ..\frontend

# Install dependencies
echo "Installing Node.js dependencies..."
call npm install

echo "Frontend setup complete!"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Open Terminal 1 (Backend):"
echo "   cd backend"
echo "   venv\Scripts\activate"
echo "   python app.py"
echo ""
echo "2. Open Terminal 2 (Frontend):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "Backend: http://127.0.0.1:5000"
echo "Frontend: http://localhost:3000"
echo ""
