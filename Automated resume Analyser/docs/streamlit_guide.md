# Streamlit Web Interface Guide

## Overview
The Streamlit web interface provides an intuitive, user-friendly way to interact with the Automated Resume Analysis System. It offers both single resume analysis and batch processing capabilities through a graphical interface.

## Features
- **Single Resume Analysis**: Analyze one resume against a job description
- **Batch Processing**: Process multiple resumes at once
- **File Upload Support**: Upload TXT, PDF, and DOCX files
- **Visual Results Display**: Color-coded match scores and detailed analysis
- **Downloadable Results**: Export results as CSV files

## Accessing the Web Interface

### Method 1: Direct Command
```bash
streamlit run src/streamlit_app.py
```

### Method 2: Using the Provided Script
```bash
./run_streamlit.sh
```

After running either command, access the application in your browser at:
- Local URL: http://localhost:8501
- Network URL: http://[your-network-ip]:8501 (if available)

## Using the Interface

### Single Resume Analysis Tab
1. **Job Description Section**:
   - Paste the job description in the text area OR
   - Upload a job description file (TXT, PDF, DOCX)

2. **Resume Section**:
   - Paste the resume text in the text area OR
   - Upload a resume file (TXT, PDF, DOCX)

3. **Analysis**:
   - Click the "Analyze Resume" button
   - View the match score and detailed analysis

### Batch Processing Tab
1. **Job Description**:
   - Paste the job description in the text area OR
   - Upload a job description file

2. **Resumes**:
   - Upload multiple resume files using the file uploader

3. **Processing**:
   - Click the "Process Resumes" button
   - View the ranked candidate list with match scores

### Results Display
- **Match Score Card**: Color-coded based on match quality (green = high, orange = medium, red = low)
- **Candidate Information**: Extracted details from the resume
- **Skills Analysis**: Required vs. candidate skills comparison
- **Detailed Analysis**: Experience and keyword matching details
- **Match Visualization**: Bar chart of match components

## Interpreting Results

### Match Scores
- **80-100%**: Excellent match
- **60-79%**: Good match
- **40-59%**: Moderate match
- **0-39%**: Low match

### Color Coding
- **Green**: High match scores (70%+)
- **Orange**: Medium match scores (40-69%)
- **Red**: Low match scores (0-39%)

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **spaCy Model Missing**: Run `python -m spacy download en_core_web_sm`
3. **File Upload Issues**: Ensure files are in supported formats (TXT, PDF, DOCX)
4. **Performance**: Large PDF files may take longer to process

### Error Messages
- **"Please provide both a job description and a resume"**: Both inputs are required for analysis
- **"Error reading file"**: File format may not be supported or file is corrupted

## Customization
The web interface can be customized by modifying `src/streamlit_app.py`:
- Adjust styling in the CSS section
- Modify scoring weights in the analysis functions
- Add new visualization components
- Extend file format support

## Security Considerations
- Uploaded files are processed in memory and not stored permanently
- No personal data is collected or transmitted
- All processing happens locally on your machine

## Feedback and Support
For issues or feature requests, please:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure the spaCy language model is downloaded
4. Report issues to the project maintainers