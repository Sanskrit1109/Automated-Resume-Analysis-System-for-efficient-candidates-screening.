"""
Setup script for Automated Resume Analysis System
"""
from setuptools import setup, find_packages

setup(
    name="automated-resume-analyzer",
    version="1.0.0",
    description="An automated resume analysis and candidate screening system using NLP",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "spacy",
        "nltk",
        "python-docx",
        "PyPDF2",
        "matplotlib",
        "seaborn"
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "resume-analyzer=main:main",
        ],
    },
)