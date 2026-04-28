#!/bin/bash

# INF232 EC2 - Setup Script
# This script sets up the application for local development

echo "================================"
echo "INF232 EC2 - Setup Script"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "Virtual environment created."
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated."
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Dependencies installed."
echo ""

# Initialize database
echo "Initializing database..."
python3 -c "from app import init_db; init_db()"
echo "Database initialized."
echo ""

echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "To start the application, run:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open your browser and navigate to:"
echo "  http://localhost:5000"
echo ""
