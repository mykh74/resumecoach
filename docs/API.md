# Resume Coach API Documentation

## Overview
FastAPI backend providing AI-powered resume coaching and job matching services.

## Base URL
```
http://localhost:8000
```

## API Endpoints

### Health Check
**GET** `/api/health`

Check service status and availability.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-07T23:20:00",
  "version": "1.0.0",
  "services": {
    "resume_parser": true,
    "job_parser": true,
    "llm_service": true
  }
}
```

---

### Upload Resume
**POST** `/api/upload-resume`

Upload and parse a PDF resume.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF file)

**Response:**
```json
{
  "session_id": "uuid-string",
  "filename": "resume.pdf",
  "file_size": 12345,
  "parsed_successfully": true,
  "contact_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "(555) 123-4567",
    "linkedin": "linkedin.com/in/johndoe"
  },
  "sections_found": ["summary", "experience", "education", "skills"]
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:8000/api/upload-resume \
  -F "file=@resume.pdf"
```

---

### Parse Job Description
**POST** `/api/parse-job`

Parse a job description text.

**Request:**
```json
{
  "job_text": "Senior Python Developer at TechCorp\n\nRESPONSIBILITIES\n- Develop backend services\n..."
}
```

**Response:**
```json
{
  "parsed_successfully": true,
  "title": "Senior Python Developer at TechCorp",
  "company": "TechCorp",
  "location": "San Francisco, CA",
  "experience_level": "Senior",
  "sections_found": ["responsibilities", "requirements", "benefits"]
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:8000/api/parse-job \
  -H "Content-Type: application/json" \
  -d '{"job_text": "Senior Python Developer..."}'
```

---

### Generate Coaching Analysis
**POST** `/api/analyze`

Generate AI coaching report comparing resume to job description.

**Request:**
- Content-Type: `application/x-www-form-urlencoded`
- Body:
  - `session_id`: Session ID from resume upload
  - `job_description`: Job description text
  - `use_multi_step`: true/false (optional, default: false)

**Response:**
```json
{
  "session_id": "uuid-string",
  "overall_fit_score": 85,
  "summary": "Strong match with some gaps in cloud technologies...",
  "gaps": [
    {
      "skill_area": "Kubernetes",
      "severity": "medium",
      "impact": "Required for the role",
      "suggestion": "Complete online course and deploy personal project"
    }
  ],
  "strengths": [
    {
      "skill_area": "Python Development",
      "relevance": "high",
      "evidence": "7 years experience with Django and Flask",
      "how_to_highlight": "Emphasize microservices projects in summary"
    }
  ],
  "recommendations": [
    {
      "action": "Add Kubernetes certifications to resume",
      "priority": "high",
      "timeline": "1-2 weeks"
    }
  ],
  "created_at": "2026-01-07T23:30:00",
  "analysis_type": "single-step"
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "session_id=your-session-id" \
  -F "job_description=Senior Python Developer..." \
  -F "use_multi_step=false"
```

---

### Get Report
**GET** `/api/reports/{session_id}`

Retrieve the last generated coaching report for a session.

**Response:** Same format as `/api/analyze`

**Example (curl):**
```bash
curl http://localhost:8000/api/reports/your-session-id
```

---

### Create Chat Session
**POST** `/api/chat/sessions`

Create a new chat session for conversational coaching.

**Request:**
- Content-Type: `application/x-www-form-urlencoded`
- Body: `session_id` (from resume upload + analysis)

**Response:**
```json
{
  "chat_session_id": "chat-uuid",
  "session_id": "original-session-id",
  "created_at": "2026-01-07T23:40:00"
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:8000/api/chat/sessions \
  -F "session_id=your-session-id"
```

---

### Send Chat Message
**POST** `/api/chat/sessions/{chat_session_id}/messages`

Send a message to the AI career coach.

**Request:**
```json
{
  "message": "What are the top 3 skills I should focus on improving?"
}
```

**Response:**
```json
{
  "session_id": "chat-uuid",
  "message": "What are the top 3 skills...",
  "response": "Based on your resume and the job requirements, I recommend focusing on:\n1. Kubernetes...",
  "timestamp": "2026-01-07T23:45:00"
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:8000/api/chat/sessions/chat-uuid/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "What skills should I improve?"}'
```

---

### Get Chat History
**GET** `/api/chat/sessions/{chat_session_id}/history`

Retrieve conversation history.

**Response:**
```json
{
  "session_id": "chat-uuid",
  "messages": [
    {
      "role": "user",
      "content": "What skills should I improve?",
      "timestamp": "2026-01-07T23:45:00"
    },
    {
      "role": "assistant",
      "content": "Based on your resume...",
      "timestamp": "2026-01-07T23:45:05"
    }
  ],
  "total_messages": 2
}
```

**Example (curl):**
```bash
curl http://localhost:8000/api/chat/sessions/chat-uuid/history
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "timestamp": "2026-01-07T23:50:00"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad request (validation error)
- `404` - Resource not found (session/chat not found)
- `422` - Unprocessable entity (invalid request format)
- `500` - Internal server error

---

## Running the Server

### Development Mode
```bash
cd /Users/michaelkuzmyn/projects/ik/ResumeCoach
source venv/bin/activate
PYTHONPATH=/Users/michaelkuzmyn/projects/ik/ResumeCoach python -m backend.api.main
```

Server will run on `http://0.0.0.0:8000` with auto-reload enabled.

### Access Interactive API Docs
Once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Complete Workflow Example

```bash
# 1. Upload resume
RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload-resume \
  -F "file=@resume.pdf")
SESSION_ID=$(echo $RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['session_id'])")

# 2. Generate analysis
curl -X POST http://localhost:8000/api/analyze \
  -F "session_id=$SESSION_ID" \
  -F "job_description=Senior Python Developer at TechCorp..." \
  -F "use_multi_step=false"

# 3. Create chat session
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/chat/sessions \
  -F "session_id=$SESSION_ID")
CHAT_ID=$(echo $CHAT_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['chat_session_id'])")

# 4. Ask follow-up questions
curl -X POST http://localhost:8000/api/chat/sessions/$CHAT_ID/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "How should I prepare for the interview?"}'

# 5. Get chat history
curl http://localhost:8000/api/chat/sessions/$CHAT_ID/history
```

---

## Testing

Run API integration tests:
```bash
PYTHONPATH=/Users/michaelkuzmyn/projects/ik/ResumeCoach pytest tests/test_api.py -v
```

---

## Architecture

- **Framework**: FastAPI 0.128.0
- **Server**: Uvicorn 0.40.0
- **Validation**: Pydantic 2.12.5
- **Storage**: In-memory (sessions dict) - will be replaced with database in production
- **LLM Provider**: OpenAI via LangChain
- **PDF Processing**: pdfplumber + PyPDF2

---

## Environment Variables

Required in `.env`:
```
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key  # optional
```

---

## Next Steps

1. Add database (PostgreSQL) for persistent session storage
2. Add authentication/authorization (JWT tokens)
3. Add rate limiting
4. Add file storage (S3) for uploaded resumes
5. Add WebSocket support for real-time chat
6. Deploy to AWS EC2/ECS
