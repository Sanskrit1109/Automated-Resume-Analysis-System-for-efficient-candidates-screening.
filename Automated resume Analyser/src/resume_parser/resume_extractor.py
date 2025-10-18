"""
Module for extracting information from resumes
"""
import re

class ResumeExtractor:
    def __init__(self, text_processor):
        """Initialize with a text processor instance"""
        self.text_processor = text_processor
    
    def extract_information(self, resume_text):
        """Extract key information from resume text"""
        info = {}
        
        # Extract name (assumed to be the first line or in a specific format)
        info['name'] = self._extract_name(resume_text)
        
        # Extract email
        info['email'] = self._extract_email(resume_text)
        
        # Extract phone number
        info['phone'] = self._extract_phone(resume_text)
        
        # Extract skills
        info['skills'] = self._extract_skills(resume_text)
        
        # Extract experience
        info['experience_years'] = self._extract_experience(resume_text)
        
        # Extract education
        info['education'] = self._extract_education(resume_text)
        
        # Extract keywords
        info['keywords'] = self.text_processor.extract_keywords(resume_text)
        
        return info
    
    def _extract_name(self, text):
        """Extract candidate name"""
        lines = text.strip().split('\n')
        if lines:
            # Assume the first line is the name
            return lines[0].strip()
        return "Unknown"
    
    def _extract_email(self, text):
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else "Not found"
    
    def _extract_phone(self, text):
        """Extract phone number"""
        phone_patterns = [
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}',
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return "Not found"
    
    def _extract_skills(self, text):
        """Extract skills section"""
        # Look for skills section
        skills_section = re.search(r'SKILLS.*?(?:\n\n|\n[A-Z]|\Z)', text, re.DOTALL | re.IGNORECASE)
        if skills_section:
            skills_text = skills_section.group()
            # Extract bullet points or list items
            skills = re.findall(r'[-•]\s*([^\n]+)', skills_text)
            if skills:
                return [skill.strip() for skill in skills]
            # If no bullet points, split by commas or newlines
            return [skill.strip() for skill in re.split(r'[,\n]', skills_text) if skill.strip()]
        
        # Alternative approach: look for common skill keywords
        skill_keywords = ['Python', 'Java', 'JavaScript', 'SQL', 'Machine Learning', 'Docker', 'AWS', 'React']
        found_skills = []
        for skill in skill_keywords:
            if skill.lower() in text.lower():
                found_skills.append(skill)
        return found_skills if found_skills else ["Not specified"]
    
    def _extract_experience(self, text):
        """Extract years of experience"""
        # Look for experience patterns
        exp_patterns = [
            r'(\d+)\s*\+?\s*years?\s*(?:of)?\s*experience',
            r'experience[^\d]{0,20}(\d+)\s*\+?\s*years?',
            r'(\d+)\s*\+?\s*years?[^\w]*experience'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Count employment entries as proxy for experience
        employment_count = len(re.findall(r'(?:experience|employment|work)[\s\S]*?(?:\d{4}|\d{2})', text, re.IGNORECASE))
        return employment_count if employment_count > 0 else 0
    
    def _extract_education(self, text):
        """Extract education information"""
        education_section = re.search(r'EDUCATION.*?(?:\n\n|\n[A-Z]|\Z)', text, re.DOTALL | re.IGNORECASE)
        if education_section:
            edu_text = education_section.group()
            # Extract degrees
            degrees = re.findall(r'(?:B\.S\.|B\.A\.|M\.S\.|M\.A\.|Ph\.D\.|Bachelor|Master|Doctorate)[^\n]*', edu_text, re.IGNORECASE)
            return degrees if degrees else ["Degree not specified"]
        
        # Fallback: look for degree keywords
        degree_keywords = ['Bachelor', 'Master', 'Ph.D', 'BS', 'MS', 'BA', 'MA']
        found_degrees = []
        for degree in degree_keywords:
            if degree.lower() in text.lower():
                found_degrees.append(degree)
        return found_degrees if found_degrees else ["Education not specified"]