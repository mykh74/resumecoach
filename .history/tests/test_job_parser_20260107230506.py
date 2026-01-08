"""
Unit tests for Job Description Parser.
"""

import pytest
from backend.services.job_parser import JobParser
from backend.models.schema import JobDescription


class TestJobParser:
    """Test cases for JobParser."""
    
    @pytest.fixture
    def parser(self):
        """Create a parser instance."""
        return JobParser()
    
    def test_parser_initialization(self, parser):
        """Test parser initializes correctly."""
        assert parser is not None
        assert hasattr(parser, 'parse_job_description')
    
    def test_parse_simple_job(self, parser):
        """Test parsing simple job description."""
        job_text = """
        Senior Python Developer at TechCorp
        
        Location: San Francisco, CA (Remote)
        Type: Full-time
        
        ABOUT THE ROLE
        We are seeking an experienced Python developer to join our team.
        
        RESPONSIBILITIES
        - Design and develop backend services
        - Write clean, maintainable code
        - Collaborate with cross-functional teams
        
        REQUIREMENTS
        - 5+ years of Python development experience
        - Strong knowledge of Django or Flask
        - Experience with AWS
        - Bachelor's degree in Computer Science
        
        PREFERRED QUALIFICATIONS
        - Experience with React
        - Knowledge of Docker and Kubernetes
        
        BENEFITS
        - Competitive salary
        - Health insurance
        - Remote work options
        """
        
        job = parser.parse_job_description(job_text)
        
        # Check basic structure
        assert isinstance(job, JobDescription)
        assert job.raw_text
        
        # Check extracted fields
        assert job.title is not None
        assert "python" in job.title.lower() or "developer" in job.title.lower()
        
        assert len(job.responsibilities) > 0
        assert len(job.requirements) > 0
        
        # Check skills
        assert len(job.required_skills) > 0 or len(job.preferred_skills) > 0
    
    def test_extract_experience_level(self, parser):
        """Test experience level extraction."""
        text_senior = "We need a senior engineer with 5+ years experience"
        text_entry = "Entry level position for recent graduates"
        
        job_senior = parser.parse_job_description(text_senior)
        job_entry = parser.parse_job_description(text_entry)
        
        assert job_senior.experience_level is not None
        assert job_entry.experience_level is not None
    
    def test_extract_job_type(self, parser):
        """Test job type extraction."""
        text_ft = "This is a full-time position"
        text_contract = "Contract role for 6 months"
        
        job_ft = parser.parse_job_description(text_ft)
        job_contract = parser.parse_job_description(text_contract)
        
        assert "full" in job_ft.job_type.lower()
        assert "contract" in job_contract.job_type.lower()
    
    def test_extract_location(self, parser):
        """Test location extraction."""
        text = "Location: New York, NY - Remote possible"
        job = parser.parse_job_description(text)
        
        assert job.location is not None
    
    def test_extract_responsibilities(self, parser):
        """Test responsibilities extraction."""
        resp_text = """
        - Write code
        - Review pull requests
        - Mentor junior developers
        """
        
        responsibilities = parser._extract_responsibilities(resp_text)
        
        assert len(responsibilities) > 0
        assert isinstance(responsibilities, list)
    
    def test_extract_skills(self, parser):
        """Test skills extraction."""
        text = "Required: Python, JavaScript, 5 years of experience with AWS"
        skills = parser._extract_skills(text, critical=True)
        
        assert len(skills) > 0
        assert any('python' in s.lower() for s in skills)
    
    def test_empty_job_description(self, parser):
        """Test handling of empty job description."""
        job = parser.parse_job_description("")
        
        assert isinstance(job, JobDescription)
        assert job.raw_text == ""
        assert len(job.responsibilities) == 0
