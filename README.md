# Automated Resume Analysis System

An automated resume analysis and candidate screening system using Natural Language Processing (NLP) to parse resumes and job descriptions, extract key information, and rank candidates based on relevance scores.

## Features
- Resume parsing and information extraction
- Job description analysis
- Semantic matching algorithms
- Candidate ranking based on relevance scores
- Skills, experience, and education matching
- Web-based user interface with Streamlit

## Technologies Used
- Python
- Natural Language Processing (NLP)
- scikit-learn
- spaCy
- pandas
- NLTK
- Streamlit (for web interface)

## Installation
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

### Command Line Interface
```python
python main.py
```

### Web Interface (Streamlit)
```bash
streamlit run src/streamlit_app.py
```

Or use the provided script:
```bash
./run_streamlit.sh
```

### Demonstration
To see an overview of the enhanced system with Streamlit:
```bash
python demo_with_streamlit.py
```

### Batch Processing
```bash
python src/batch_processor.py --resumes-dir data/resumes --job-description data/job_descriptions/software_engineer.txt
```