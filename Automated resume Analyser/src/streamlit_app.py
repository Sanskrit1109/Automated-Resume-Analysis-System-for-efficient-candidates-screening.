"""
Streamlit Web Application for Automated Resume Analysis System
"""
import sys
import os
import streamlit as st
import pandas as pd
from io import StringIO

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nlp_processor.text_processor import TextProcessor
from resume_parser.resume_extractor import ResumeExtractor
from job_matcher.matcher import JobMatcher
from utils.file_handler import read_file

# Set page configuration
st.set_page_config(
    page_title="Automated Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2196F3;
        margin-bottom: 1rem;
    }
    .result-card {
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .match-high {
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
    }
    .match-medium {
        background-color: #FFF3E0;
        border-left: 5px solid #FF9800;
    }
    .match-low {
        background-color: #FFEBEE;
        border-left: 5px solid #F44336;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main header
    st.markdown("<h1 class='main-header'>Automated Resume Analysis System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Efficient candidate screening using Natural Language Processing</p>", unsafe_allow_html=True)
    
    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["📄 Single Resume Analysis", "📋 Batch Processing", "ℹ️ About"])
    
    with tab1:
        single_resume_analysis()
    
    with tab2:
        batch_processing()
    
    with tab3:
        show_about()

def single_resume_analysis():
    st.markdown("<h2 class='sub-header'>Single Resume Analysis</h2>", unsafe_allow_html=True)
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Job Description")
        job_description = st.text_area(
            "Enter the job description:",
            height=300,
            placeholder="Paste the job description here..."
        )
        
        # File uploader for job description file
        job_file = st.file_uploader(
            "Or upload a job description file (TXT, PDF, DOCX):",
            type=["txt", "pdf", "docx"],
            key="job_file"
        )
        
        if job_file is not None:
            # Read job description from file
            job_description = read_file_from_upload(job_file)
    
    with col2:
        st.subheader("Resume")
        resume_text = st.text_area(
            "Enter the resume text:",
            height=300,
            placeholder="Paste the resume text here..."
        )
        
        # File uploader for resume file
        resume_file = st.file_uploader(
            "Or upload a resume file (TXT, PDF, DOCX):",
            type=["txt", "pdf", "docx"],
            key="resume_file"
        )
        
        if resume_file is not None:
            # Read resume from file
            resume_text = read_file_from_upload(resume_file)
    
    # Analysis button
    if st.button("Analyze Resume", type="primary", use_container_width=True):
        if not job_description or not resume_text:
            st.warning("Please provide both a job description and a resume.")
            return
        
        with st.spinner("Analyzing resume..."):
            try:
                # Initialize components
                text_processor = TextProcessor()
                resume_extractor = ResumeExtractor(text_processor)
                job_matcher = JobMatcher(text_processor)
                
                # Extract resume information
                resume_info = resume_extractor.extract_information(resume_text)
                
                # Calculate match score
                match_score = job_matcher.calculate_match_score(resume_text, job_description)
                
                # Get detailed analysis
                analysis = job_matcher.detailed_analysis(resume_text, job_description)
                
                # Display results
                display_single_analysis_results(resume_info, match_score, analysis)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

def display_single_analysis_results(resume_info, match_score, analysis):
    st.markdown("<h2 class='sub-header'>Analysis Results</h2>", unsafe_allow_html=True)
    
    # Match score card
    score_class = get_score_class(match_score)
    st.markdown(f"""
    <div class="result-card {score_class}">
        <h3>Match Score: {match_score:.2f}%</h3>
        <p>{get_score_description(match_score)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different result sections
    result_tab1, result_tab2, result_tab3, result_tab4 = st.tabs([
        "📋 Candidate Info", 
        "🎯 Skills Analysis", 
        "🔍 Detailed Analysis", 
        "📈 Match Visualization"
    ])
    
    with result_tab1:
        st.subheader("Candidate Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Name:**", resume_info.get('name', 'N/A'))
            st.write("**Email:**", resume_info.get('email', 'N/A'))
            st.write("**Phone:**", resume_info.get('phone', 'N/A'))
            st.write("**Experience:**", f"{resume_info.get('experience_years', 0)} years")
        
        with col2:
            st.write("**Education:**")
            for edu in resume_info.get('education', []):
                st.write(f"- {edu}")
            
            st.write("**Skills:**")
            for skill in resume_info.get('skills', []):
                st.write(f"- {skill}")
    
    with result_tab2:
        st.subheader("Skills Analysis")
        st.write("**Required Skills:**")
        for skill in analysis.get('required_skills', []):
            st.write(f"- {skill}")
        
        st.write("**Candidate Skills:**")
        for skill in analysis.get('candidate_skills', []):
            st.write(f"- {skill}")
        
        st.write("**Matched Skills:**")
        for skill in analysis.get('matched_skills', []):
            st.write(f"- ✅ {skill}")
        
        st.write("**Missing Skills:**")
        for skill in analysis.get('missing_skills', []):
            st.write(f"- ❌ {skill}")
        
        st.progress(analysis.get('skill_match_percentage', 0) / 100)
        st.write(f"**Skill Match Percentage:** {analysis.get('skill_match_percentage', 0):.2f}%")
    
    with result_tab3:
        st.subheader("Detailed Analysis")
        st.write("**Experience Requirements:**")
        st.write(f"- Required: {analysis.get('required_experience', 0)} years")
        st.write(f"- Candidate: {analysis.get('candidate_experience', 0)} years")
        st.write(f"- Match: {'✅' if analysis.get('experience_match', False) else '❌'}")
        
        st.write("**Keyword Similarity:**")
        st.write(f"- Score: {analysis.get('keyword_similarity', 0):.2f}%")
    
    with result_tab4:
        st.subheader("Match Visualization")
        # Create a simple bar chart for match components
        match_data = {
            'Component': ['Skills', 'Keywords', 'Experience'],
            'Score': [
                analysis.get('skill_match_percentage', 0),
                analysis.get('keyword_similarity', 0),
                100 if analysis.get('experience_match', False) else 0
            ]
        }
        df = pd.DataFrame(match_data)
        st.bar_chart(df.set_index('Component'))

def batch_processing():
    st.markdown("<h2 class='sub-header'>Batch Resume Processing</h2>", unsafe_allow_html=True)
    
    # Job description input
    st.subheader("Job Description")
    job_description = st.text_area(
        "Enter the job description for batch processing:",
        height=200,
        placeholder="Paste the job description here..."
    )
    
    job_file = st.file_uploader(
        "Or upload a job description file:",
        type=["txt", "pdf", "docx"],
        key="batch_job_file"
    )
    
    if job_file is not None:
        job_description = read_file_from_upload(job_file)
    
    # Resume files uploader
    st.subheader("Resumes")
    resume_files = st.file_uploader(
        "Upload multiple resume files:",
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True,
        key="batch_resume_files"
    )
    
    if st.button("Process Resumes", type="primary", use_container_width=True):
        if not job_description:
            st.warning("Please provide a job description.")
            return
        
        if not resume_files:
            st.warning("Please upload at least one resume file.")
            return
        
        with st.spinner(f"Processing {len(resume_files)} resumes..."):
            try:
                # Initialize components
                text_processor = TextProcessor()
                resume_extractor = ResumeExtractor(text_processor)
                job_matcher = JobMatcher(text_processor)
                
                # Process each resume
                results = []
                for resume_file in resume_files:
                    try:
                        # Read resume from file
                        resume_text = read_file_from_upload(resume_file)
                        
                        # Extract information
                        resume_info = resume_extractor.extract_information(resume_text)
                        
                        # Calculate match score
                        match_score = job_matcher.calculate_match_score(resume_text, job_description)
                        
                        # Get detailed analysis
                        analysis = job_matcher.detailed_analysis(resume_text, job_description)
                        
                        # Store results
                        result = {
                            'candidate': resume_info.get('name', resume_file.name),
                            'email': resume_info.get('email', 'N/A'),
                            'match_score': round(match_score, 2),
                            'skills_matched': len(analysis.get('matched_skills', [])),
                            'skills_missing': len(analysis.get('missing_skills', []))
                        }
                        results.append(result)
                    
                    except Exception as e:
                        st.warning(f"Error processing {resume_file.name}: {str(e)}")
                        continue
                
                # Sort results by match score
                results.sort(key=lambda x: x['match_score'], reverse=True)
                
                # Display results
                display_batch_results(results)
                
            except Exception as e:
                st.error(f"An error occurred during batch processing: {str(e)}")

def display_batch_results(results):
    st.markdown("<h2 class='sub-header'>Batch Processing Results</h2>", unsafe_allow_html=True)
    
    if not results:
        st.info("No results to display.")
        return
    
    # Summary statistics
    st.subheader("Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Candidates", len(results))
    
    with col2:
        st.metric("Average Score", f"{sum(r['match_score'] for r in results) / len(results):.2f}%")
    
    with col3:
        st.metric("Highest Score", f"{max(r['match_score'] for r in results):.2f}%")
    
    with col4:
        st.metric("Top Candidate", results[0]['candidate'] if results else "N/A")
    
    # Results table
    st.subheader("Candidate Ranking")
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(results)
    
    # Apply styling to the dataframe
    def highlight_scores(val):
        if isinstance(val, (int, float)) and 'match_score' in str(val).lower() or 'score' in str(val).lower():
            if val >= 70:
                return 'background-color: #E8F5E9; color: #2E7D32'
            elif val >= 40:
                return 'background-color: #FFF3E0; color: #EF6C00'
            else:
                return 'background-color: #FFEBEE; color: #C62828'
        return ''
    
    # Display the styled dataframe
    st.dataframe(df.style.applymap(highlight_scores), use_container_width=True)
    
    # Download button for results
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="resume_analysis_results.csv",
        mime="text/csv",
        use_container_width=True
    )

def show_about():
    st.markdown("<h2 class='sub-header'>About This System</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    ### Automated Resume Analysis System
    
    This system uses Natural Language Processing (NLP) to streamline the candidate screening process. 
    It parses resumes and job descriptions, extracts key information, and uses semantic matching 
    algorithms to calculate relevance scores and rank candidates.
    
    #### Key Features:
    - **NLP-Based Text Processing**: Uses spaCy, NLTK, and scikit-learn for semantic analysis
    - **Resume Information Extraction**: Parses candidate details, skills, experience, and education
    - **Job Matching Algorithm**: Calculates relevance scores using weighted metrics
    - **Batch Processing**: Process multiple resumes simultaneously
    - **Comprehensive Reporting**: Generates ranked candidate lists with detailed matching analysis
    
    #### Technologies Used:
    - **Python**: Core programming language
    - **spaCy**: Industrial-strength NLP library for text processing
    - **NLTK**: Natural language toolkit for text preprocessing
    - **scikit-learn**: Machine learning library for TF-IDF and similarity calculations
    - **Streamlit**: Web application framework
    
    #### Benefits:
    - **Time Efficiency**: Reduces manual screening time by up to 80%
    - **Consistency**: Standardized evaluation criteria
    - **Scalability**: Process hundreds of resumes quickly
    - **Accuracy**: Semantic matching improves candidate-job alignment
    - **Data-Driven**: Objective scoring based on job requirements
    """, unsafe_allow_html=True)

def read_file_from_upload(uploaded_file):
    """Read content from uploaded file"""
    try:
        # For text files
        if uploaded_file.type == "text/plain":
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            return stringio.read()
        
        # For other file types, save temporarily and read
        else:
            # Save file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Read file content
            content = read_file(temp_path)
            
            # Remove temporary file
            os.remove(temp_path)
            
            return content
    except Exception as e:
        st.error(f"Error reading file {uploaded_file.name}: {str(e)}")
        return ""

def get_score_class(score):
    """Get CSS class based on match score"""
    if score >= 70:
        return "match-high"
    elif score >= 40:
        return "match-medium"
    else:
        return "match-low"

def get_score_description(score):
    """Get description based on match score"""
    if score >= 80:
        return "Excellent match! This candidate closely aligns with the job requirements."
    elif score >= 60:
        return "Good match. This candidate meets most of the job requirements."
    elif score >= 40:
        return "Moderate match. This candidate has some relevant skills and experience."
    else:
        return "Low match. This candidate may not be the best fit for this position."

if __name__ == "__main__":
    main()