"""
Unit tests for the Automated Resume Analysis System
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from nlp_processor.text_processor import TextProcessor
from resume_parser.resume_extractor import ResumeExtractor
from job_matcher.matcher import JobMatcher

class TestResumeAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.text_processor = TextProcessor()
        self.resume_extractor = ResumeExtractor(self.text_processor)
        self.job_matcher = JobMatcher(self.text_processor)
        
        self.sample_resume = """
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
        
        self.sample_job_description = """
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
    
    def test_text_preprocessing(self):
        """Test text preprocessing functionality"""
        text = "Hello, World! This is a Test."
        processed = self.text_processor.preprocess_text(text)
        # Should remove punctuation and stopwords
        self.assertIsInstance(processed, str)
    
    def test_resume_extraction(self):
        """Test resume information extraction"""
        info = self.resume_extractor.extract_information(self.sample_resume)
        self.assertIn('name', info)
        self.assertIn('email', info)
        self.assertIn('skills', info)
        self.assertEqual(info['name'], 'John Doe')
    
    def test_skill_extraction(self):
        """Test skill extraction from resume"""
        skills = self.resume_extractor._extract_skills(self.sample_resume)
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)
    
    def test_match_calculation(self):
        """Test match score calculation"""
        score = self.job_matcher.calculate_match_score(self.sample_resume, self.sample_job_description)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 100.0)
    
    def test_detailed_analysis(self):
        """Test detailed analysis functionality"""
        analysis = self.job_matcher.detailed_analysis(self.sample_resume, self.sample_job_description)
        self.assertIsInstance(analysis, dict)
        self.assertIn('required_skills', analysis)
        self.assertIn('candidate_skills', analysis)

if __name__ == '__main__':
    unittest.main()