"""
Unit tests for Resume Parser.
"""

import pytest
from pathlib import Path
from backend.services.resume_parser import ResumeParser
from backend.models.schema import Resume


class TestResumeParser:
    """Test cases for ResumeParser."""
    
    @pytest.fixture
    def parser(self):
        """Create a parser instance."""
        return ResumeParser()
    
    def test_parser_initialization(self, parser):
        """Test parser initializes correctly."""
        assert parser is not None
        assert hasattr(parser, 'parse_text')
        assert hasattr(parser, 'parse_pdf')
    
    def test_parse_simple_text(self, parser):
        """Test parsing simple resume text."""
        resume_text = """
        John Doe
        john.doe@email.com | (555) 123-4567
        linkedin.com/in/johndoe
        
        SUMMARY
        Experienced software engineer with 5 years of Python development.
        
        SKILLS
        Python, JavaScript, React, SQL, AWS, Docker
        
        EXPERIENCE
        Senior Software Engineer
        Tech Company Inc.
        January 2020 - Present
        - Developed microservices using Python and Flask
        - Led team of 3 developers
        - Improved system performance by 40%
        
        EDUCATION
        Bachelor of Science in Computer Science
        University of Technology
        2018
        """
        
        resume = parser.parse_text(resume_text)
        
        # Check basic structure
        assert isinstance(resume, Resume)
        assert resume.raw_text
        
        # Check contact info
        assert resume.contact_info.name == "John Doe"
        assert resume.contact_info.email == "john.doe@email.com"
        assert resume.contact_info.phone is not None
        
        # Check sections
        assert len(resume.skills) > 0
        assert "Python" in resume.skills or any("python" in s.lower() for s in resume.skills)
        
        assert len(resume.experiences) > 0
        assert resume.experiences[0].title is not None
        
        assert len(resume.education) > 0
        assert resume.education[0].degree is not None
    
    def test_clean_text(self, parser):
        """Test text cleaning."""
        messy_text = "  Test    with   extra   spaces  \n\n\n  and   newlines  "
        cleaned = parser._clean_text(messy_text)
        
        assert "  " not in cleaned  # No double spaces
        assert cleaned == cleaned.strip()  # No leading/trailing whitespace
    
    def test_extract_contact_email(self, parser):
        """Test email extraction."""
        text = "Contact me at test.user@example.com for more info"
        contact = parser._extract_contact_info(text, "")
        
        assert contact.email == "test.user@example.com"
    
    def test_extract_skills(self, parser):
        """Test skills extraction."""
        skills_text = "Python, Java, JavaScript, React, Node.js, SQL, AWS"
        skills = parser._extract_skills(skills_text)
        
        assert len(skills) > 0
        assert isinstance(skills, list)
        assert all(isinstance(skill, str) for skill in skills)
    
    def test_empty_resume(self, parser):
        """Test handling of empty resume."""
        resume = parser.parse_text("")
        
        assert isinstance(resume, Resume)
        assert resume.raw_text == ""
        assert len(resume.skills) == 0
        assert len(resume.experiences) == 0
    
    def test_section_identification(self, parser):
        """Test section identification."""
        text = """
        EXPERIENCE
        Some experience content
        
        EDUCATION
        Some education content
        
        SKILLS
        Some skills content
        """
        
        sections = parser._identify_sections(text)
        
        assert 'experience' in sections
        assert 'education' in sections
        assert 'skills' in sections
