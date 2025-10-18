#!/bin/bash

# Script to run the Streamlit Resume Analyzer App

echo "Starting Automated Resume Analysis System with Streamlit..."
echo "========================================================"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing/Updating dependencies..."
    pip install -r requirements.txt
fi

# Download spaCy model if not present
echo "Checking for spaCy language model..."
python -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null || {
    echo "Downloading spaCy English language model..."
    python -m spacy download en_core_web_sm
}

# Run the Streamlit app
echo "Starting Streamlit application..."
echo "Access the app at: http://localhost:8501"
streamlit run src/streamlit_app.py
