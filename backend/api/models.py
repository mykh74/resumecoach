"""
API Request and Response Models

Defines Pydantic models for API request/response validation.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


# Request Models
class JobDescriptionRequest(BaseModel):
    """Request body for job description parsing."""
    job_text: str = Field(..., min_length=50, description="Raw job description text")


class AnalyzeRequest(BaseModel):
    """Request body for generating coaching report."""
    resume_text: Optional[str] = Field(None, description="Resume text (if not uploaded as file)")
    job_description: str = Field(..., min_length=50, description="Job description text")
    use_multi_step: bool = Field(False, description="Use multi-step analysis approach")


class ChatMessageRequest(BaseModel):
    """Request body for chat message."""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    session_id: Optional[str] = Field(None, description="Existing chat session ID")


# Response Models
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    version: str
    services: dict


class ResumeUploadResponse(BaseModel):
    """Response after resume upload."""
    session_id: str
    filename: str
    file_size: int
    parsed_successfully: bool
    contact_info: Optional[dict] = None
    sections_found: List[str] = []


class JobParseResponse(BaseModel):
    """Response after job description parsing."""
    parsed_successfully: bool
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    experience_level: Optional[str] = None
    sections_found: List[str] = []


class AnalysisResponse(BaseModel):
    """Response for coaching analysis."""
    session_id: str
    overall_fit_score: int
    summary: str
    gaps: List[dict]
    strengths: List[dict]
    recommendations: List[dict]
    created_at: datetime
    analysis_type: str  # "single-step" or "multi-step"


class ChatResponse(BaseModel):
    """Response for chat message."""
    session_id: str
    message: str
    response: str
    timestamp: datetime


class ChatHistoryResponse(BaseModel):
    """Response for chat history."""
    session_id: str
    messages: List[dict]
    total_messages: int


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime
