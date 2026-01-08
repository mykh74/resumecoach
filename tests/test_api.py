"""
API Integration Tests

Tests for FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.services.resume_parser import ResumeParser
from backend.services.job_parser import JobParser
from backend.services.llm_service import LLMService
import backend.api.main as main_module

# Initialize services for testing
@pytest.fixture(scope="module", autouse=True)
def initialize_services():
    """Initialize services before running tests."""
    main_module.resume_parser = ResumeParser()
    main_module.job_parser = JobParser()
    main_module.llm_service = LLMService(provider="openai")
    yield
    # Cleanup after tests
    main_module.resume_parser = None
    main_module.job_parser = None
    main_module.llm_service = None


client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_check(self):
        """Test health endpoint returns correct status."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "services" in data
        assert data["services"]["resume_parser"] is True
        assert data["services"]["job_parser"] is True
        assert data["services"]["llm_service"] is True


class TestJobParsingEndpoint:
    """Tests for job description parsing."""
    
    def test_parse_job_description(self):
        """Test job description parsing endpoint."""
        job_text = """
        Senior Python Developer at TechCorp
        
        Location: San Francisco, CA
        Type: Full-time
        
        RESPONSIBILITIES
        - Design and develop backend services
        - Write clean, maintainable code
        
        REQUIREMENTS
        - 5+ years of Python development experience
        - Strong knowledge of Django or Flask
        """
        
        response = client.post(
            "/api/parse-job",
            json={"job_text": job_text}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["parsed_successfully"] is True
        assert data["title"] is not None
        assert "python" in data["title"].lower() or "developer" in data["title"].lower()
    
    def test_parse_job_empty_text(self):
        """Test parsing with empty text returns error."""
        response = client.post(
            "/api/parse-job",
            json={"job_text": ""}
        )
        
        assert response.status_code == 422  # Validation error


class TestAnalysisEndpoints:
    """Tests for analysis endpoints."""
    
    def test_analyze_without_session(self):
        """Test analysis without valid session returns error."""
        response = client.post(
            "/api/analyze",
            data={
                "session_id": "invalid-session-id",
                "job_description": "Software Engineer position requiring Python skills.",
                "use_multi_step": False
            }
        )
        
        assert response.status_code == 404
        assert "Session not found" in response.json()["detail"]


class TestChatEndpoints:
    """Tests for chat endpoints."""
    
    def test_create_chat_without_session(self):
        """Test creating chat without valid session returns error."""
        response = client.post(
            "/api/chat/sessions",
            data={"session_id": "invalid-session-id"}
        )
        
        assert response.status_code == 404
    
    def test_send_message_invalid_chat(self):
        """Test sending message to invalid chat session."""
        response = client.post(
            "/api/chat/sessions/invalid-chat-id/messages",
            json={"message": "Hello"}
        )
        
        assert response.status_code == 404
    
    def test_get_history_invalid_chat(self):
        """Test getting history for invalid chat session."""
        response = client.get("/api/chat/sessions/invalid-chat-id/history")
        assert response.status_code == 404
