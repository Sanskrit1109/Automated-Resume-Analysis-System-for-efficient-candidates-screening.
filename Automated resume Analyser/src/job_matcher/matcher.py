"""
Job matching module for calculating relevance scores between resumes and job descriptions
"""
import re

class JobMatcher:
    def __init__(self, text_processor):
        """Initialize with a text processor instance"""
        self.text_processor = text_processor
    
    def calculate_match_score(self, resume_text, job_description):
        """Calculate overall match score between resume and job description"""
        # Calculate multiple similarity metrics
        keyword_similarity = self._calculate_keyword_similarity(resume_text, job_description)
        skill_match = self._calculate_skill_match(resume_text, job_description)
        experience_match = self._calculate_experience_match(resume_text, job_description)
        
        # Weighted average of all metrics
        # Adjust weights based on importance
        total_score = (
            keyword_similarity * 0.4 +  # 40% weight
            skill_match * 0.4 +         # 40% weight
            experience_match * 0.2      # 20% weight
        )
        
        return min(total_score * 100, 100)  # Convert to percentage (0-100)
    
    def _calculate_keyword_similarity(self, resume_text, job_description):
        """Calculate similarity based on keywords"""
        return self.text_processor.calculate_similarity(resume_text, job_description)
    
    def _calculate_skill_match(self, resume_text, job_description):
        """Calculate skill match score"""
        # Extract skills from job description
        required_skills = self._extract_required_skills(job_description)
        if not required_skills:
            return 1.0  # No skills required
        
        # Extract skills from resume
        candidate_skills = self._extract_candidate_skills(resume_text)
        
        # Calculate match ratio
        matched_skills = set()
        for req_skill in required_skills:
            for cand_skill in candidate_skills:
                if req_skill.lower() in cand_skill.lower() or cand_skill.lower() in req_skill.lower():
                    matched_skills.add(req_skill)
                    break
        
        return len(matched_skills) / len(required_skills)
    
    def _calculate_experience_match(self, resume_text, job_description):
        """Calculate experience match score"""
        # Extract required experience from job description
        required_exp = self._extract_required_experience(job_description)
        if required_exp <= 0:
            return 1.0  # No experience required
        
        # Extract candidate experience from resume
        candidate_exp = self._extract_candidate_experience(resume_text)
        
        # Calculate match (capped at 1.0)
        return min(candidate_exp / required_exp, 1.0)
    
    def _extract_required_skills(self, job_description):
        """Extract required skills from job description"""
        # Look for skills section in job description
        skills_section = re.search(r'(?:requirements?|skills?|qualifications?).*?(?:\n\n|\n[A-Z]|\Z)', 
                                 job_description, re.DOTALL | re.IGNORECASE)
        
        skills = []
        if skills_section:
            skills_text = skills_section.group()
            # Extract bullet points or list items
            extracted_skills = re.findall(r'[-•]\s*([^\n]+)', skills_text)
            if extracted_skills:
                skills = [skill.strip() for skill in extracted_skills]
            else:
                # Split by commas or newlines
                skills = [skill.strip() for skill in re.split(r'[,\n]', skills_text) 
                         if skill.strip() and len(skill.strip()) > 2]
        
        # If no skills found, look for common skill keywords
        if not skills:
            skill_keywords = ['Python', 'Java', 'JavaScript', 'SQL', 'Machine Learning', 
                            'Docker', 'AWS', 'React', 'Node.js', 'Angular', 'Vue']
            for skill in skill_keywords:
                if skill.lower() in job_description.lower():
                    skills.append(skill)
        
        return skills
    
    def _extract_candidate_skills(self, resume_text):
        """Extract candidate skills from resume"""
        # Look for skills section in resume
        skills_section = re.search(r'SKILLS.*?(?:\n\n|\n[A-Z]|\Z)', resume_text, re.DOTALL | re.IGNORECASE)
        
        skills = []
        if skills_section:
            skills_text = skills_section.group()
            # Extract bullet points or list items
            extracted_skills = re.findall(r'[-•]\s*([^\n]+)', skills_text)
            if extracted_skills:
                skills = [skill.strip() for skill in extracted_skills]
            else:
                # Split by commas or newlines
                skills = [skill.strip() for skill in re.split(r'[,\n]', skills_text) 
                         if skill.strip() and len(skill.strip()) > 2]
        
        return skills
    
    def _extract_required_experience(self, job_description):
        """Extract required years of experience from job description"""
        exp_patterns = [
            r'(\d+)\s*\+?\s*years?\s*(?:of)?\s*(?:experience|work)',
            r'(?:experience|work).*?(\d+)\s*\+?\s*years?',
            r'minimum.*?(\d+)\s*\+?\s*years?',
            r'required.*?(\d+)\s*\+?\s*years?'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return 0  # No experience requirement found
    
    def _extract_candidate_experience(self, resume_text):
        """Extract candidate's years of experience from resume"""
        # Look for explicit experience mention
        exp_patterns = [
            r'(\d+)\s*\+?\s*years?\s*(?:of)?\s*(?:experience|work)',
            r'(?:experience|work).*?(\d+)\s*\+?\s*years?',
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, resume_text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Count employment entries as proxy
        employment_entries = re.findall(r'(?:experience|employment|work)[\s\S]*?(?:\d{4}|\d{2})', resume_text, re.IGNORECASE)
        return len(employment_entries)
    
    def detailed_analysis(self, resume_text, job_description):
        """Provide detailed analysis of the match"""
        analysis = {}
        
        # Skill match details
        required_skills = self._extract_required_skills(job_description)
        candidate_skills = self._extract_candidate_skills(resume_text)
        
        matched_skills = []
        missing_skills = []
        
        for req_skill in required_skills:
            found = False
            for cand_skill in candidate_skills:
                if req_skill.lower() in cand_skill.lower() or cand_skill.lower() in req_skill.lower():
                    matched_skills.append(req_skill)
                    found = True
                    break
            if not found:
                missing_skills.append(req_skill)
        
        analysis['required_skills'] = required_skills
        analysis['candidate_skills'] = candidate_skills
        analysis['matched_skills'] = matched_skills
        analysis['missing_skills'] = missing_skills
        analysis['skill_match_percentage'] = (len(matched_skills) / len(required_skills) * 100) if required_skills else 100
        
        # Experience details
        required_exp = self._extract_required_experience(job_description)
        candidate_exp = self._extract_candidate_experience(resume_text)
        analysis['required_experience'] = required_exp
        analysis['candidate_experience'] = candidate_exp
        analysis['experience_match'] = (candidate_exp >= required_exp)
        
        # Keyword similarity
        keyword_similarity = self._calculate_keyword_similarity(resume_text, job_description)
        analysis['keyword_similarity'] = round(keyword_similarity * 100, 2)
        
        return analysis