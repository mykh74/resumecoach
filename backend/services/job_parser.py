"""
Job Description Parser - Extracts and structures information from job postings.
Identifies requirements, responsibilities, and key criteria.
"""

import re
from typing import List, Dict, Optional
from backend.models.schema import JobDescription, JobRequirement


class JobParser:
    """Parse job descriptions and extract structured information."""
    
    # Common section patterns
    SECTION_PATTERNS = {
        'responsibilities': r'(responsibilities|duties|what you\'ll do|role|job description)',
        'requirements': r'(requirements|qualifications|what we\'re looking for|must have|you have)',
        'preferred': r'(preferred|nice to have|bonus|plus|ideal)',
        'benefits': r'(benefits|perks|what we offer|compensation)',
        'about': r'(about us|about the company|company overview)',
    }
    
    # Experience level indicators
    EXPERIENCE_LEVELS = {
        'entry': r'(entry.level|junior|0-2\s+years|graduate|recent grad)',
        'mid': r'(mid.level|3-5\s+years|intermediate)',
        'senior': r'(senior|lead|5\+?\s+years|6-8\s+years|expert)',
        'principal': r'(principal|staff|8\+?\s+years|10\+?\s+years)',
    }
    
    def __init__(self):
        """Initialize job parser."""
        pass
    
    def parse_job_description(self, text: str) -> JobDescription:
        """
        Parse job description text and extract structured information.
        
        Args:
            text: Raw job description text
            
        Returns:
            JobDescription object with structured data
        """
        # Clean text
        text = self._clean_text(text)
        
        # Extract basic information
        title = self._extract_title(text)
        company = self._extract_company(text)
        location = self._extract_location(text)
        job_type = self._extract_job_type(text)
        experience_level = self._extract_experience_level(text)
        salary_range = self._extract_salary(text)
        
        # Extract sections
        sections = self._identify_sections(text)
        
        # Extract structured data
        summary = self._extract_summary(text, sections.get('about', ''))
        responsibilities = self._extract_responsibilities(sections.get('responsibilities', ''))
        requirements = self._extract_requirements(
            sections.get('requirements', ''),
            sections.get('preferred', '')
        )
        required_skills = self._extract_skills(sections.get('requirements', ''), critical=True)
        preferred_skills = self._extract_skills(sections.get('preferred', ''), critical=False)
        benefits = self._extract_benefits(sections.get('benefits', ''))
        
        return JobDescription(
            raw_text=text,
            title=title,
            company=company,
            location=location,
            job_type=job_type,
            experience_level=experience_level,
            salary_range=salary_range,
            summary=summary,
            responsibilities=responsibilities,
            requirements=requirements,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            benefits=benefits,
            metadata={'sections_found': list(sections.keys())}
        )
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        return text.strip()
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify sections in the job description."""
        sections = {}
        lines = text.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check for section headers
            section_found = None
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line_lower, re.IGNORECASE) and len(line.split()) <= 10:
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
    
    def _extract_title(self, text: str) -> Optional[str]:
        """Extract job title (usually in first few lines)."""
        lines = text.split('\n')[:10]
        
        # Look for common job title patterns
        for line in lines:
            line = line.strip()
            # Job titles often have keywords like Engineer, Manager, etc.
            if any(keyword in line.lower() for keyword in [
                'engineer', 'developer', 'manager', 'analyst', 'scientist',
                'designer', 'architect', 'consultant', 'specialist', 'coordinator'
            ]):
                if 3 <= len(line.split()) <= 8:  # Reasonable length
                    return line
        
        # Fallback: return first non-empty line
        for line in lines:
            if line.strip() and len(line.strip()) > 5:
                return line.strip()
        
        return None
    
    def _extract_company(self, text: str) -> Optional[str]:
        """Extract company name."""
        # Look for "at CompanyName" or "CompanyName is hiring"
        match = re.search(r'at\s+([A-Z][A-Za-z0-9\s&]+?)(?:\s+is|\s+in|\s*-|\n)', text[:500])
        if match:
            return match.group(1).strip()
        
        # Look for "Company: Name"
        match = re.search(r'Company:?\s*([A-Z][A-Za-z0-9\s&]+)', text[:500], re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        return None
    
    def _extract_location(self, text: str) -> Optional[str]:
        """Extract job location."""
        # Look for "Location:" or city patterns
        match = re.search(r'Location:?\s*([A-Za-z\s,]+(?:Remote|Hybrid)?)', text[:500], re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Look for Remote/Hybrid indicators
        if re.search(r'\b(Remote|Hybrid|Work from home)\b', text[:500], re.IGNORECASE):
            return "Remote"
        
        return None
    
    def _extract_job_type(self, text: str) -> Optional[str]:
        """Extract job type (full-time, part-time, contract, etc.)."""
        text_lower = text[:500].lower()
        
        if 'full-time' in text_lower or 'full time' in text_lower:
            return "Full-time"
        elif 'part-time' in text_lower or 'part time' in text_lower:
            return "Part-time"
        elif 'contract' in text_lower:
            return "Contract"
        elif 'intern' in text_lower:
            return "Internship"
        
        return "Full-time"  # Default assumption
    
    def _extract_experience_level(self, text: str) -> Optional[str]:
        """Extract experience level."""
        text_lower = text.lower()
        
        for level, pattern in self.EXPERIENCE_LEVELS.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                return level.capitalize()
        
        return None
    
    def _extract_salary(self, text: str) -> Optional[str]:
        """Extract salary range if mentioned."""
        # Look for salary patterns
        match = re.search(r'\$\s*\d+[,\d]*\s*[-to]+\s*\$?\s*\d+[,\d]*', text)
        if match:
            return match.group(0)
        
        # Look for annual salary
        match = re.search(r'\$\s*\d+[,\d]*k?(?:\s*per\s*year|\s*annually)?', text, re.IGNORECASE)
        if match:
            return match.group(0)
        
        return None
    
    def _extract_summary(self, full_text: str, about_section: str) -> Optional[str]:
        """Extract job summary."""
        if about_section and len(about_section.strip()) > 50:
            # Take first paragraph of about section
            paragraphs = about_section.split('\n\n')
            if paragraphs:
                return paragraphs[0].strip()[:500]
        
        # Fallback: take first few lines
        lines = [l.strip() for l in full_text.split('\n')[:10] if l.strip()]
        if len(lines) > 3:
            return ' '.join(lines[1:4])[:500]
        
        return None
    
    def _extract_responsibilities(self, responsibilities_section: str) -> List[str]:
        """Extract list of responsibilities."""
        if not responsibilities_section:
            return []
        
        responsibilities = []
        
        # Split by bullets, numbers, or newlines
        items = re.split(r'[•\-\*\n]+|\d+\.', responsibilities_section)
        
        for item in items:
            item = item.strip()
            if item and 10 <= len(item) <= 500:  # Reasonable length
                responsibilities.append(item)
        
        return responsibilities[:15]  # Limit number
    
    def _extract_requirements(self, requirements_section: str, preferred_section: str) -> List[JobRequirement]:
        """Extract structured requirements."""
        requirements = []
        
        # Process required section
        if requirements_section:
            items = re.split(r'[•\-\*\n]+|\d+\.', requirements_section)
            for item in items:
                item = item.strip()
                if item and 5 <= len(item) <= 500:
                    # Determine importance based on keywords
                    importance = "critical" if any(kw in item.lower() for kw in ['must', 'required', 'essential']) else "high"
                    requirements.append(JobRequirement(
                        category="required",
                        requirement=item,
                        importance=importance
                    ))
        
        # Process preferred section
        if preferred_section:
            items = re.split(r'[•\-\*\n]+|\d+\.', preferred_section)
            for item in items:
                item = item.strip()
                if item and 5 <= len(item) <= 500:
                    requirements.append(JobRequirement(
                        category="preferred",
                        requirement=item,
                        importance="medium"
                    ))
        
        return requirements[:30]  # Reasonable limit
    
    def _extract_skills(self, section_text: str, critical: bool = True) -> List[str]:
        """Extract skills from text."""
        if not section_text:
            return []
        
        skills = []
        
        # Common technical skills patterns
        tech_skills = re.findall(
            r'\b(Python|Java|JavaScript|C\+\+|Ruby|Go|Rust|Swift|Kotlin|'
            r'SQL|NoSQL|MongoDB|PostgreSQL|MySQL|Redis|'
            r'AWS|Azure|GCP|Docker|Kubernetes|'
            r'React|Angular|Vue|Node\.js|Django|Flask|'
            r'Machine Learning|Deep Learning|AI|NLP|Computer Vision|'
            r'Git|CI/CD|Agile|Scrum|REST|API|'
            r'TensorFlow|PyTorch|Scikit-learn)\b',
            section_text,
            re.IGNORECASE
        )
        
        skills.extend(tech_skills)
        
        # Look for "X years of experience with Y"
        exp_matches = re.findall(
            r'(\d+\+?)\s*years?\s*(?:of\s*)?(?:experience\s*)?(?:with|in)\s+([A-Za-z0-9\.\s]+?)(?:\s+and|\s+or|,|\.|$)',
            section_text,
            re.IGNORECASE
        )
        
        for years, skill in exp_matches:
            if skill.strip() and len(skill.strip()) < 50:
                skills.append(f"{skill.strip()} ({years}+ years)")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower not in seen:
                seen.add(skill_lower)
                unique_skills.append(skill)
        
        return unique_skills[:25]  # Limit
    
    def _extract_benefits(self, benefits_section: str) -> List[str]:
        """Extract benefits list."""
        if not benefits_section:
            return []
        
        benefits = []
        
        # Split by bullets or newlines
        items = re.split(r'[•\-\*\n]+', benefits_section)
        
        for item in items:
            item = item.strip()
            if item and 5 <= len(item) <= 200:
                benefits.append(item)
        
        return benefits[:20]  # Reasonable limit
