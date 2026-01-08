"""
FastAPI Main Application

Backend API for Resume Coach application.
Provides endpoints for resume parsing, job analysis, and AI coaching.
"""
import os
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from backend.services.resume_parser import ResumeParser
from backend.services.job_parser import JobParser
from backend.services.llm_service import LLMService
from backend.api.models import (
    HealthResponse,
    JobDescriptionRequest,
    AnalyzeRequest,
    ChatMessageRequest,
    ResumeUploadResponse,
    JobParseResponse,
    AnalysisResponse,
    ChatResponse,
    ChatHistoryResponse,
    ErrorResponse
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application version
VERSION = "1.0.0"

# Global service instances
resume_parser: Optional[ResumeParser] = None
job_parser: Optional[JobParser] = None
llm_service: Optional[LLMService] = None

# Session storage (in-memory for now, will be replaced with database later)
sessions = {}
chat_sessions = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    global resume_parser, job_parser, llm_service
    
    logger.info("Initializing services...")
    resume_parser = ResumeParser()
    job_parser = JobParser()
    llm_service = LLMService(provider="openai")
    logger.info("Services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down services...")


# Create FastAPI app
app = FastAPI(
    title="Resume Coach API",
    description="AI-powered resume coaching and job matching service",
    version=VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            timestamp=datetime.now()
        ).model_dump(mode='json')
    )


# Health check endpoint
@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns service status and availability.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=VERSION,
        services={
            "resume_parser": resume_parser is not None,
            "job_parser": job_parser is not None,
            "llm_service": llm_service is not None
        }
    )


# Resume upload endpoint
@app.post("/api/upload-resume", response_model=ResumeUploadResponse, tags=["Resume"])
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume PDF file.
    
    Returns parsed resume data and a session ID for further operations.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse resume
        logger.info(f"Parsing resume: {file.filename}")
        parsed_resume = resume_parser.parse_pdf(temp_path)
        
        # Generate session ID
        import uuid
        session_id = str(uuid.uuid4())
        
        # Store in session
        sessions[session_id] = {
            "resume": parsed_resume,
            "filename": file.filename,
            "uploaded_at": datetime.now()
        }
        
        # Clean up temp file
        os.remove(temp_path)
        
        # Prepare response
        contact_dict = None
        if parsed_resume.contact_info:
            contact_dict = {
                "name": parsed_resume.contact_info.name,
                "email": parsed_resume.contact_info.email,
                "phone": parsed_resume.contact_info.phone,
                "linkedin": parsed_resume.contact_info.linkedin
            }
        
        return ResumeUploadResponse(
            session_id=session_id,
            filename=file.filename,
            file_size=len(content),
            parsed_successfully=True,
            contact_info=contact_dict,
            sections_found=parsed_resume.metadata.get('sections_found', [])
        )
        
    except Exception as e:
        logger.error(f"Error parsing resume: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")


# Job description parsing endpoint
@app.post("/api/parse-job", response_model=JobParseResponse, tags=["Job"])
async def parse_job_description(request: JobDescriptionRequest):
    """
    Parse a job description text.
    
    Returns structured job information.
    """
    try:
        logger.info("Parsing job description")
        parsed_job = job_parser.parse_job_description(request.job_text)
        
        return JobParseResponse(
            parsed_successfully=True,
            title=parsed_job.title,
            company=parsed_job.company,
            location=parsed_job.location,
            experience_level=parsed_job.experience_level,
            sections_found=parsed_job.metadata.get('sections_found', [])
        )
        
    except Exception as e:
        logger.error(f"Error parsing job description: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to parse job: {str(e)}")


# Analysis endpoint
@app.post("/api/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_resume(
    session_id: str = Form(...),
    job_description: str = Form(...),
    use_multi_step: bool = Form(False)
):
    """
    Generate AI coaching report comparing resume to job description.
    
    Requires a session_id from a previous resume upload.
    """
    try:
        # Retrieve session
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found. Please upload resume first.")
        
        session = sessions[session_id]
        resume = session["resume"]
        
        # Parse job description
        logger.info("Parsing job description for analysis")
        parsed_job = job_parser.parse_job_description(job_description)
        
        # Generate coaching report
        logger.info(f"Generating coaching report (multi_step={use_multi_step})")
        if use_multi_step:
            report = llm_service.generate_coaching_report_multi_step(
                resume=resume,
                job_description=parsed_job,
                session_id=session_id
            )
        else:
            report = llm_service.generate_coaching_report(
                resume=resume,
                job_description=parsed_job,
                session_id=session_id
            )
        
        # Store report in session
        session["last_report"] = report
        session["job_description"] = parsed_job
        session["analyzed_at"] = datetime.now()
        
        # Convert to response format
        gaps_list = [
            {
                "skill_area": gap.skill_area,
                "severity": gap.severity,
                "impact": gap.impact,
                "suggestion": gap.suggestion
            }
            for gap in report.gaps
        ]
        
        strengths_list = [
            {
                "skill_area": strength.skill_area,
                "relevance": strength.relevance,
                "evidence": strength.evidence,
                "how_to_highlight": strength.how_to_highlight
            }
            for strength in report.strengths
        ]
        
        recommendations_list = [
            {
                "action": rec.action,
                "priority": rec.priority,
                "timeline": rec.timeline
            }
            for rec in report.recommendations
        ]
        
        return AnalysisResponse(
            session_id=session_id,
            overall_fit_score=report.overall_fit_score,
            summary=report.summary,
            gaps=gaps_list,
            strengths=strengths_list,
            recommendations=recommendations_list,
            created_at=datetime.now(),
            analysis_type="multi-step" if use_multi_step else "single-step"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# Get analysis report
@app.get("/api/reports/{session_id}", response_model=AnalysisResponse, tags=["Analysis"])
async def get_report(session_id: str):
    """
    Retrieve the last generated coaching report for a session.
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    if "last_report" not in session:
        raise HTTPException(status_code=404, detail="No report found for this session")
    
    report = session["last_report"]
    
    # Convert to response format
    gaps_list = [
        {
            "skill_area": gap.skill_area,
            "severity": gap.severity,
            "impact": gap.impact,
            "suggestion": gap.suggestion
        }
        for gap in report.gaps
    ]
    
    strengths_list = [
        {
            "skill_area": strength.skill_area,
            "relevance": strength.relevance,
            "evidence": strength.evidence,
            "how_to_highlight": strength.how_to_highlight
        }
        for strength in report.strengths
    ]
    
    recommendations_list = [
        {
            "action": rec.action,
            "priority": rec.priority,
            "timeline": rec.timeline
        }
        for rec in report.recommendations
    ]
    
    return AnalysisResponse(
        session_id=session_id,
        overall_fit_score=report.overall_fit_score,
        summary=report.summary,
        gaps=gaps_list,
        strengths=strengths_list,
        recommendations=recommendations_list,
        created_at=session.get("analyzed_at", datetime.now()),
        analysis_type="unknown"
    )


# Create chat session
@app.post("/api/chat/sessions", response_model=dict, tags=["Chat"])
async def create_chat_session(session_id: str = Form(...)):
    """
    Create a new chat session linked to an analysis session.
    
    Requires an existing session_id with analyzed resume/job.
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    if "last_report" not in session or "job_description" not in session:
        raise HTTPException(
            status_code=400,
            detail="Please complete analysis before starting chat"
        )
    
    # Initialize chat history
    import uuid
    chat_id = str(uuid.uuid4())
    chat_sessions[chat_id] = {
        "session_id": session_id,
        "messages": [],
        "created_at": datetime.now()
    }
    
    return {
        "chat_session_id": chat_id,
        "session_id": session_id,
        "created_at": datetime.now()
    }


# Send chat message
@app.post("/api/chat/sessions/{chat_session_id}/messages", response_model=ChatResponse, tags=["Chat"])
async def send_chat_message(chat_session_id: str, request: ChatMessageRequest):
    """
    Send a message to the AI career coach.
    
    Returns AI response with coaching advice.
    """
    if chat_session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    chat_session = chat_sessions[chat_session_id]
    session_id = chat_session["session_id"]
    session = sessions[session_id]
    
    try:
        # Get conversation history
        conversation_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in chat_session["messages"]
        ]
        
        # Generate response
        logger.info(f"Generating chat response for session {chat_session_id}")
        response = llm_service.chat_response(
            message=request.message,
            conversation_history=conversation_history,
            resume=session["resume"],
            job_description=session["job_description"],
            session_id=session_id
        )
        
        # Store messages
        chat_session["messages"].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now()
        })
        chat_session["messages"].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now()
        })
        
        return ChatResponse(
            session_id=chat_session_id,
            message=request.message,
            response=response,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


# Get chat history
@app.get("/api/chat/sessions/{chat_session_id}/history", response_model=ChatHistoryResponse, tags=["Chat"])
async def get_chat_history(chat_session_id: str):
    """
    Retrieve chat conversation history.
    """
    if chat_session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    chat_session = chat_sessions[chat_session_id]
    
    messages = [
        {
            "role": msg["role"],
            "content": msg["content"],
            "timestamp": msg["timestamp"]
        }
        for msg in chat_session["messages"]
    ]
    
    return ChatHistoryResponse(
        session_id=chat_session_id,
        messages=messages,
        total_messages=len(messages)
    )


# Run server
if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
