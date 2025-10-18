"""
Demonstration script for the Automated Resume Analysis System with Streamlit enhancement
"""
import os
import sys
import subprocess
import time

def main():
    print("Automated Resume Analysis System - Enhanced with Streamlit")
    print("=" * 60)
    print("This script demonstrates the enhanced capabilities of the system")
    print("including the new Streamlit web interface.\n")
    
    # Show project structure
    print("Project Structure:")
    print("-" * 20)
    show_project_structure()
    
    # Show key features
    print("\nKey Features:")
    print("-" * 15)
    show_features()
    
    # Show usage options
    print("\nUsage Options:")
    print("-" * 15)
    show_usage_options()
    
    # Offer to start Streamlit app
    print("\n" + "=" * 60)
    start_streamlit = input("Would you like to start the Streamlit web interface? (y/n): ")
    
    if start_streamlit.lower() in ['y', 'yes']:
        start_streamlit_app()
    else:
        print("You can start the Streamlit app later with:")
        print("  streamlit run src/streamlit_app.py")
        print("  or")
        print("  ./run_streamlit.sh")

def show_project_structure():
    """Show the enhanced project structure"""
    structure = """
    src/
    ├── main.py                 # Main application entry point
    ├── batch_processor.py      # Batch processing of multiple resumes
    ├── streamlit_app.py        # Streamlit web interface (NEW)
    ├── nlp_processor/
    │   ├── __init__.py
    │   └── text_processor.py   # NLP processing utilities
    ├── resume_parser/
    │   ├── __init__.py
    │   └── resume_extractor.py # Resume information extraction
    ├── job_matcher/
    │   ├── __init__.py
    │   └── matcher.py          # Job matching algorithms
    ├── utils/
    │   ├── __init__.py
    │   └── file_handler.py     # File format handling
    └── visualization/
        ├── __init__.py
        └── dashboard.py        # Results visualization
    """
    print(structure)

def show_features():
    """Show the enhanced features"""
    features = [
        "📄 NLP-Based Text Processing with spaCy and scikit-learn",
        "🔍 Resume Information Extraction (skills, experience, education)",
        "🎯 Job Matching Algorithm with weighted scoring",
        "📋 Batch Processing for multiple resumes",
        "🌐 Streamlit Web Interface for easy interaction (NEW)",
        "📊 Visual Results Display with color-coded scores (NEW)",
        "📤 File Upload Support (TXT, PDF, DOCX) (NEW)",
        "💾 Downloadable Results in CSV format (NEW)",
        "📈 Data Visualization and Reporting"
    ]
    
    for feature in features:
        print(f"  {feature}")

def show_usage_options():
    """Show usage options"""
    options = [
        "Command Line Interface:",
        "  python src/main.py                           # Single resume analysis",
        "  python src/batch_processor.py --resumes-dir data/resumes --job-description data/job_descriptions/software_engineer.txt  # Batch processing",
        "",
        "Web Interface (Streamlit):",
        "  streamlit run src/streamlit_app.py          # Start web interface",
        "  ./run_streamlit.sh                          # Alternative script"
    ]
    
    for option in options:
        print(f"  {option}")

def start_streamlit_app():
    """Start the Streamlit application"""
    print("\nStarting Streamlit web interface...")
    print("Please wait while the application initializes...")
    print("\nOnce started, access the app in your browser at:")
    print("  Local URL: http://localhost:8501")
    
    try:
        # Change to project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Start Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "src/streamlit_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit app: {e}")
    except KeyboardInterrupt:
        print("\nStreamlit app stopped.")

if __name__ == "__main__":
    main()