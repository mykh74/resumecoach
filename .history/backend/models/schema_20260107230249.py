"""
Data models for Resume Coach application.
Defines structured data for resumes, job descriptions, and coaching reports.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ContactInfo(BaseModel):
    """Contact information from resume."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


class Experience(BaseModel):
    """Work experience entry."""
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)


class Education(BaseModel):
    """Education entry."""
    degree: Optional[str] = None
    institution: Optional[str] = None
    location: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: List[str] = Field(default_factory=list)


class Resume(BaseModel):
    """Parsed resume data structure."""
    raw_text: str
    contact_info: ContactInfo = Field(default_factory=ContactInfo)
    summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    experiences: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    awards: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class JobRequirement(BaseModel):
    """Job requirement entry."""
    category: str  # e.g., "required", "preferred", "nice-to-have"
    requirement: str
    importance: str = "medium"  # low, medium, high, critical


class JobDescription(BaseModel):
    """Parsed job description data structure."""
    raw_text: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None  # full-time, part-time, contract, etc.
    experience_level: Optional[str] = None  # entry, mid, senior, etc.
    salary_range: Optional[str] = None
    summary: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)
    requirements: List[JobRequirement] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    benefits: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GapAnalysis(BaseModel):
    """Analysis of gaps between resume and job requirements."""
    missing_skills: List[str] = Field(default_factory=list)
    missing_qualifications: List[str] = Field(default_factory=list)
    experience_gap: Optional[str] = None
    recommendations: List[str] = Field(default_factory=list)


class StrengthAnalysis(BaseModel):
    """Analysis of candidate strengths."""
    matching_skills: List[str] = Field(default_factory=list)
    unique_strengths: List[str] = Field(default_factory=list)
    relevant_experiences: List[str] = Field(default_factory=list)
    highlights: List[str] = Field(default_factory=list)


class CoachingReport(BaseModel):
    """Complete coaching report."""
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Overall assessment
    fit_score: float = Field(ge=0.0, le=10.0, description="Overall fit score (0-10)")
    overall_assessment: str
    
    # Detailed analysis
    gap_analysis: GapAnalysis
    strength_analysis: StrengthAnalysis
    
    # Advice sections
    resume_improvements: List[str] = Field(default_factory=list)
    interview_tips: List[str] = Field(default_factory=list)
    action_items: List[str] = Field(default_factory=list)
    general_advice: List[str] = Field(default_factory=list)
    
    # Metadata
    resume_summary: Optional[str] = None
    job_summary: Optional[str] = None
    model_used: Optional[str] = None
    processing_time: Optional[float] = None


class ChatMessage(BaseModel):
    """Chat message in conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatSession(BaseModel):
    """Chat session data."""
    session_id: str
    resume: Optional[Resume] = None
    job_description: Optional[JobDescription] = None
    coaching_report: Optional[CoachingReport] = None
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
