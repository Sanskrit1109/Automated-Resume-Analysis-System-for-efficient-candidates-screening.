"""
Main application for the Automated Resume Analysis System
"""
import os
import pandas as pd
from nlp_processor.text_processor import TextProcessor
from resume_parser.resume_extractor import ResumeExtractor
from job_matcher.matcher import JobMatcher
from utils.file_handler import read_file, save_results

def main():
    print("Automated Resume Analysis System")
    print("=" * 40)
    
    # Initialize components
    text_processor = TextProcessor()
    resume_extractor = ResumeExtractor(text_processor)
    job_matcher = JobMatcher(text_processor)
    
    # Example usage
    # In a real application, you would load resumes and job descriptions from files
    sample_resume = """
    John Doe
    Software Engineer
    Email: john.doe@example.com
    Phone: (555) 123-4567
    
    SUMMARY
    Experienced software engineer with 5 years of experience in Python, JavaScript, and cloud technologies.
    
    SKILLS
    - Python
    - JavaScript
    - AWS
    - Docker
    - Machine Learning
    - SQL
    
    EXPERIENCE
    Senior Software Engineer, Tech Corp (2020-Present)
    - Developed machine learning models for customer analytics
    - Implemented REST APIs using Flask and Django
    - Containerized applications using Docker
    
    Software Engineer, Startup Inc (2018-2020)
    - Built web applications with React and Node.js
    - Optimized database queries improving performance by 40%
    
    EDUCATION
    M.S. Computer Science, University of Technology (2018)
    B.S. Software Engineering, State University (2016)
    """
    
    sample_job_description = """
    Senior Python Developer
    
    We are looking for an experienced Python developer to join our team. The ideal candidate will have:
    
    REQUIREMENTS
    - 5+ years of experience with Python
    - Experience with machine learning frameworks
    - Knowledge of cloud platforms (AWS preferred)
    - Experience with Docker and containerization
    - Strong SQL skills
    - Bachelor's degree in Computer Science or related field
    
    RESPONSIBILITIES
    - Develop and maintain machine learning models
    - Build scalable web applications
    - Collaborate with cross-functional teams
    - Optimize application performance
    """
    
    # Extract information from resume
    print("Extracting resume information...")
    resume_info = resume_extractor.extract_information(sample_resume)
    print("Resume Information:")
    for key, value in resume_info.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 40)
    
    # Calculate match score
    print("Calculating match score...")
    match_score = job_matcher.calculate_match_score(sample_resume, sample_job_description)
    print(f"Match Score: {match_score:.2f}%")
    
    # Get detailed matching analysis
    print("\nDetailed Analysis:")
    analysis = job_matcher.detailed_analysis(sample_resume, sample_job_description)
    for key, value in analysis.items():
        print(f"  {key}: {value}")

def analyze_resumes_from_directory(resumes_dir, job_description_file):
    """Analyze multiple resumes against a job description"""
    # Initialize components
    text_processor = TextProcessor()
    resume_extractor = ResumeExtractor(text_processor)
    job_matcher = JobMatcher(text_processor)
    
    # Read job description
    job_description = read_file(job_description_file)
    
    # Results storage
    results = []
    
    # Process each resume
    for filename in os.listdir(resumes_dir):
        if filename.endswith(('.txt', '.pdf', '.docx')):
            print(f"Processing {filename}...")
            file_path = os.path.join(resumes_dir, filename)
            
            try:
                # Read resume
                resume_text = read_file(file_path)
                
                # Extract information
                resume_info = resume_extractor.extract_information(resume_text)
                
                # Calculate match score
                match_score = job_matcher.calculate_match_score(resume_text, job_description)
                
                # Get detailed analysis for skills matching
                analysis = job_matcher.detailed_analysis(resume_text, job_description)
                
                # Store results
                result = {
                    'candidate': resume_info.get('name', 'Unknown'),
                    'email': resume_info.get('email', 'Unknown'),
                    'match_score': round(match_score, 2),
                    'skills_matched': len(analysis.get('matched_skills', []))
                }
                results.append(result)
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    # Sort results by match score
    results.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Display results
    print("\n" + "=" * 50)
    print("CANDIDATE RANKING")
    print("=" * 50)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['candidate']} - Match Score: {result['match_score']}%")
    
    # Save results
    output_file = "candidate_ranking.csv"
    save_results(results, output_file)
    
    return results

if __name__ == "__main__":
    main()