#!/bin/bash

# Automated Resume Analysis System Runner

echo "Automated Resume Analysis System"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Display usage options
echo ""
echo "Usage options:"
echo "1. Run single resume analysis: python src/main.py"
echo "2. Run batch processing: python src/batch_processor.py --resumes-dir data/resumes --job-description data/job_descriptions/software_engineer.txt"
echo "3. Run unit tests: python -m pytest tests/ -v"
echo ""
echo "To run the system, use one of the commands above."

# Keep the script running
exec $SHELL