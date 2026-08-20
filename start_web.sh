#!/bin/bash

echo "🏦 Bank Statement Processor - Web Application"
echo "=============================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if models exist
if [ ! -f "models/classifier.joblib" ] || [ ! -f "models/vectorizer.joblib" ]; then
    echo "⚠️  ML models not found. Training models..."
    python scripts/generate_training_data.py
    python scripts/train_classifier.py
    echo "✅ Models trained successfully!"
    echo ""
fi

# Create necessary directories
mkdir -p uploads outputs logs

echo "🚀 Starting web server..."
echo ""
echo "Access the application at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
