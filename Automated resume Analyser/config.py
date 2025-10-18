"""
Configuration file for the Automated Resume Analysis System
"""

# NLP Processing Configuration
NLP_CONFIG = {
    'language': 'en',
    'min_keyword_length': 3,
    'max_keywords': 20,
    'similarity_threshold': 0.7
}

# Matching Algorithm Weights
MATCHING_WEIGHTS = {
    'keywords': 0.4,
    'skills': 0.4,
    'experience': 0.2
}

# File Processing Configuration
FILE_CONFIG = {
    'supported_formats': ['.txt', '.pdf', '.docx'],
    'encoding': 'utf-8'
}

# Output Configuration
OUTPUT_CONFIG = {
    'default_format': 'csv',
    'columns': [
        'candidate_name',
        'email',
        'match_score',
        'skills_matched',
        'experience_years',
        'top_keywords'
    ]
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'resume_analyzer.log'
}