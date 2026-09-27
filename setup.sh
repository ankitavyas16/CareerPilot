#!/bin/bash

# CareerPilot AI Setup Script

echo "======================================"
echo "CareerPilot AI - Setup"
echo "======================================"

echo "Checking Python version..."
python3 --version || { echo "Python 3 not found!"; exit 1; }

echo "Creating virtual environment..."
cd backend || exit 1
python3 -m venv venv

echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
	source venv/Scripts/activate
else
	source venv/bin/activate
fi

echo "Installing requirements..."
pip install -r requirements.txt

if [ ! -f .env ]; then
	echo "Creating .env file..."
	cp .env.example .env
	echo "Please edit .env and add your OpenAI API key"
fi

echo ""
echo "======================================"
echo "Setup complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your OpenAI API key"
echo "2. Run: python -m uvicorn app.main:app --reload"
echo "3. Open frontend/index.html in your browser"
