"""
Resume Parser - Extracts and structures information from PDF resumes.
Supports multiple resume formats and layouts.
"""

import re
from typing import Dict, List, Optional, Tuple
import PyPDF2
import pdfplumber
from pathlib import Path

from backend.models.schema import (
    Resume, ContactInfo, Experience, Education
)


class ResumeParser:
    """Parse PDF resumes and extract structured information."""
    
    # Common section headers (case-insensitive patterns)
    SECTION_PATTERNS = {
        'contact': r'(contact|personal\s+information)',
        'summary': r'(summary|profile|objective|about\s+me)',
        'experience': r'(experience|work\s+history|employment|professional\s+experience)',
        'education': r'(education|academic|qualifications)',
        'skills': r'(skills|technical\s+skills|competencies|expertise)',
        'projects': r'(projects|portfolio)',
        'certifications': r'(certifications?|certificates?|licenses?)',
        'awards': r'(awards?|honors?|achievements?)',
        'languages': r'(languages?)',
    }
    
    def __init__(self):
        """Initialize the resume parser."""
        pass
    
    def parse_pdf(self, file_path: str) -> Resume:
        """
        Parse a PDF resume file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Resume object with structured data
        """
        # Extract text from PDF
        text = self._extract_text_from_pdf(file_path)
        
        # Parse the resume
        return self.parse_text(text)
    
    def parse_text(self, text: str) -> Resume:
        """
        Parse resume text and extract structured information.
        
        Args:
            text: Raw resume text
            
        Returns:
            Resume object with structured data
        """
        # Clean the text
        text = self._clean_text(text)
        
        # Extract sections
        sections = self._identify_sections(text)
        
        # Parse each section
        contact_info = self._extract_contact_info(text, sections.get('contact', ''))
        summary = self._extract_summary(sections.get('summary', ''))
        skills = self._extract_skills(sections.get('skills', ''))
        experiences = self._extract_experiences(sections.get('experience', ''))
        education = self._extract_education(sections.get('education', ''))
        certifications = self._extract_list_items(sections.get('certifications', ''))
        projects = self._extract_list_items(sections.get('projects', ''))
        awards = self._extract_list_items(sections.get('awards', ''))
        languages = self._extract_list_items(sections.get('languages', ''))
        
        return Resume(
            raw_text=text,
            contact_info=contact_info,
            summary=summary,
            skills=skills,
            experiences=experiences,
            education=education,
            certifications=certifications,
            projects=projects,
            awards=awards,
            languages=languages,
            metadata={'sections_found': list(sections.keys())}
        )
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using multiple methods."""
        text = ""
        
        try:
            # Try pdfplumber first (better for complex layouts)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed: {e}, trying PyPDF2...")
            
            # Fallback to PyPDF2
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                print(f"PyPDF2 also failed: {e2}")
                raise ValueError(f"Could not extract text from PDF: {file_path}")
        
        return text
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might cause issues
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        return text.strip()
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """
        Identify sections in the resume text.
        
        Returns:
            Dictionary mapping section names to their content
        """
        sections = {}
        lines = text.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line is a section header
            section_found = None
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line_lower) and len(line.split()) <= 5:
                    section_found = section_name
                    break
            
            if section_found:
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = section_found
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _extract_contact_info(self, full_text: str, contact_section: str) -> ContactInfo:
        """Extract contact information."""
        # Combine full text and contact section for better extraction
        search_text = (full_text[:500] + "\n" + contact_section)[:1000]
        
        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', search_text)
        email = email_match.group(0) if email_match else None
        
        # Phone
        phone_match = re.search(r'(\+\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}', search_text)
        phone = phone_match.group(0) if phone_match else None
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', search_text, re.IGNORECASE)
        linkedin = linkedin_match.group(0) if linkedin_match else None
        
        # GitHub
        github_match = re.search(r'github\.com/[\w-]+', search_text, re.IGNORECASE)
        github = github_match.group(0) if github_match else None
        
        # Name (usually in first few lines)
        lines = search_text.split('\n')[:5]
        name = None
        for line in lines:
            line = line.strip()
            # Name is likely a line with 2-4 words, all capitalized, no special chars
            if 2 <= len(line.split()) <= 4 and re.match(r'^[A-Z][a-zA-Z\s]+$', line):
                name = line
                break
        
        return ContactInfo(
            name=name,
            email=email,
            phone=phone,
            linkedin=linkedin,
            github=github
        )
    
    def _extract_summary(self, summary_section: str) -> Optional[str]:
        """Extract professional summary."""
        if summary_section and len(summary_section.strip()) > 20:
            return summary_section.strip()
        return None
    
    def _extract_skills(self, skills_section: str) -> List[str]:
        """Extract skills list."""
        if not skills_section:
            return []
        
        skills = []
        
        # Split by common delimiters
        skill_text = re.sub(r'[•\-\*\n]', ',', skills_section)
        potential_skills = [s.strip() for s in skill_text.split(',')]
        
        for skill in potential_skills:
            if skill and 2 <= len(skill) <= 50:  # Reasonable skill length
                skills.append(skill)
        
        return skills[:50]  # Limit to reasonable number
    
    def _extract_experiences(self, experience_section: str) -> List[Experience]:
        """Extract work experiences."""
        if not experience_section:
            return []
        
        experiences = []
        
        # Split by date patterns or company indicators
        # This is a simplified version - could be enhanced
        blocks = re.split(r'\n(?=\d{4}|\w+\s+\d{4})', experience_section)
        
        for block in blocks:
            if len(block.strip()) < 20:
                continue
            
            lines = [l.strip() for l in block.split('\n') if l.strip()]
            
            if len(lines) < 2:
                continue
            
            # First line often contains title and company
            title = lines[0] if lines else None
            company = lines[1] if len(lines) > 1 else None
            
            # Look for dates
            date_match = re.search(r'(\w+\s+\d{4})\s*[-–to]+\s*(\w+\s+\d{4}|Present|Current)', block, re.IGNORECASE)
            start_date = date_match.group(1) if date_match else None
            end_date = date_match.group(2) if date_match else None
            
            # Responsibilities are typically bullet points
            responsibilities = []
            for line in lines[2:]:
                if line and not re.match(r'^\d{4}', line):
                    responsibilities.append(line)
            
            experiences.append(Experience(
                title=title,
                company=company,
                start_date=start_date,
                end_date=end_date,
                description=block[:200],
                responsibilities=responsibilities[:10]  # Limit bullets
            ))
        
        return experiences[:10]  # Limit number of jobs
    
    def _extract_education(self, education_section: str) -> List[Education]:
        """Extract education information."""
        if not education_section:
            return []
        
        education_list = []
        
        # Split by potential degree indicators
        blocks = re.split(r'\n(?=Bachelor|Master|PhD|B\.S\.|M\.S\.|MBA)', education_section, flags=re.IGNORECASE)
        
        for block in blocks:
            if len(block.strip()) < 10:
                continue
            
            lines = [l.strip() for l in block.split('\n') if l.strip()]
            
            degree = lines[0] if lines else None
            institution = lines[1] if len(lines) > 1 else None
            
            # Look for graduation date
            date_match = re.search(r'\b(19|20)\d{2}\b', block)
            graduation_date = date_match.group(0) if date_match else None
            
            # Look for GPA
            gpa_match = re.search(r'GPA:?\s*(\d\.\d+)', block, re.IGNORECASE)
            gpa = gpa_match.group(1) if gpa_match else None
            
            education_list.append(Education(
                degree=degree,
                institution=institution,
                graduation_date=graduation_date,
                gpa=gpa
            ))
        
        return education_list[:5]  # Limit entries
    
    def _extract_list_items(self, section_text: str) -> List[str]:
        """Extract list items from a section."""
        if not section_text:
            return []
        
        items = []
        
        # Split by bullets, dashes, newlines
        parts = re.split(r'[•\-\*\n]+', section_text)
        
        for part in parts:
            part = part.strip()
            if part and 5 <= len(part) <= 200:
                items.append(part)
        
        return items[:20]  # Reasonable limit
