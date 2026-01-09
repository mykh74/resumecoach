# ResumeCoach API Documentation

**Version:** 1.0  
**Base URL:** `https://api.resumecoach.com`  
**Protocol:** HTTPS  
**Authentication:** None (Public API)

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Authentication](#authentication)
4. [API Endpoints](#api-endpoints)
5. [Request/Response Format](#requestresponse-format)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Code Examples](#code-examples)

---

## 🎯 Overview

The ResumeCoach API provides AI-powered resume analysis and optimization services. It allows developers to integrate resume parsing, job description analysis, and LLM-powered recommendations into their applications.

### Key Features

- **Resume Parsing**: Extract structured data from PDF resumes
- **Job Analysis**: Parse job descriptions and identify requirements
- **AI Recommendations**: Generate personalized improvement suggestions
- **Interactive Chat**: Ask follow-up questions about your resume
- **Multi-Provider LLM**: Switch between OpenAI and AWS SageMaker
- **Session Management**: Track multiple analysis sessions

### Base URL

- **Production**: `https://api.resumecoach.com`
- **Local Development**: `http://localhost:8000`

### OpenAPI Documentation

Interactive API documentation is available at:
- **Swagger UI**: `https://api.resumecoach.com/docs`
- **ReDoc**: `https://api.resumecoach.com/redoc`

---

## 🚀 Quick Start

### Example Workflow

```python
import requests

BASE_URL = "https://api.resumecoach.com"

# 1. Upload resume
with open("resume.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{BASE_URL}/api/upload-resume", files=files)
    session_id = response.json()["session_id"]

# 2. Parse job description
job_data = {
    "job_description": "Software Engineer with 3+ years Python experience..."
}
response = requests.post(f"{BASE_URL}/api/parse-job", json=job_data)
job_requirements = response.json()

# 3. Generate analysis
analysis_data = {
    "session_id": session_id,
    "job_title": "Software Engineer",
    "company_name": "TechCorp"
}
response = requests.post(f"{BASE_URL}/api/analyze", json=analysis_data)
report = response.json()

print(report["analysis"])
```

---

## 🔐 Authentication

**Current Version**: No authentication required (public API)

**Future Versions**: API keys will be required for production use

```http
Authorization: Bearer YOUR_API_KEY
```

---

## 📡 API Endpoints

### Health & Status

#### GET /api/health

Check API health status.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-08T12:00:00Z"
}
```

---

### Resume Operations

#### POST /api/upload-resume

Upload and parse a PDF resume.

**Request**:
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: 
  - `file`: PDF file (max 10 MB)

**cURL Example**:
```bash
curl -X POST https://api.resumecoach.com/api/upload-resume \
  -F "file=@resume.pdf"
```

**Response** (200 OK):
```json
{
  "message": "Resume uploaded and parsed successfully",
  "session_id": "abc123xyz",
  "resume_data": {
    "contact_info": {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "(555) 123-4567",
      "location": "San Francisco, CA",
      "linkedin": "linkedin.com/in/johndoe",
      "github": "github.com/johndoe"
    },
    "skills": [
      "Python",
      "JavaScript",
      "AWS",
      "Docker",
      "FastAPI"
    ],
    "experience": [
      {
        "title": "Senior Software Engineer",
        "company": "TechCorp",
        "dates": "2020 - Present",
        "description": "Led development of microservices..."
      }
    ],
    "education": [
      {
        "degree": "BS Computer Science",
        "institution": "University of California",
        "year": "2018"
      }
    ]
  }
}
```

**Errors**:
- `422`: Invalid file format or missing file
- `413`: File too large (>10 MB)
- `500`: Processing error

---

#### GET /api/session/{session_id}

Retrieve resume data for a specific session.

**Parameters**:
- `session_id` (path): Session identifier from upload

**cURL Example**:
```bash
curl https://api.resumecoach.com/api/session/abc123xyz
```

**Response** (200 OK):
```json
{
  "session_id": "abc123xyz",
  "resume_data": {
    "contact_info": { ... },
    "skills": [ ... ],
    "experience": [ ... ],
    "education": [ ... ]
  },
  "job_data": {
    "title": "Software Engineer",
    "required_skills": [ ... ]
  }
}
```

**Errors**:
- `404`: Session not found
- `500`: Retrieval error

---

### Job Analysis

#### POST /api/parse-job

Parse a job description and extract requirements.

**Request**:
- Method: `POST`
- Content-Type: `application/json`
- Body:
```json
{
  "job_description": "Software Engineer with 3+ years of Python experience. Required: FastAPI, AWS, Docker. Preferred: Kubernetes, CI/CD."
}
```

**cURL Example**:
```bash
curl -X POST https://api.resumecoach.com/api/parse-job \
  -H "Content-Type: application/json" \
  -d '{"job_description": "Software Engineer..."}'
```

**Response** (200 OK):
```json
{
  "job_title": "Software Engineer",
  "required_skills": [
    "Python (3+ years)",
    "FastAPI",
    "AWS",
    "Docker"
  ],
  "preferred_skills": [
    "Kubernetes",
    "CI/CD"
  ],
  "required_qualifications": [
    "3+ years of experience",
    "Bachelor's degree in Computer Science"
  ],
  "responsibilities": [
    "Develop and maintain microservices",
    "Design scalable systems",
    "Collaborate with cross-functional teams"
  ]
}
```

**Errors**:
- `422`: Empty or invalid job description
- `500`: Parsing error

---

### Analysis & Recommendations

#### POST /api/analyze

Generate AI-powered resume analysis and recommendations.

**Request**:
- Method: `POST`
- Content-Type: `application/json`
- Body:
```json
{
  "session_id": "abc123xyz",
  "job_title": "Software Engineer",
  "company_name": "TechCorp",
  "job_description": "Software Engineer with 3+ years...",
  "provider": "openai"  // optional: "openai" or "sagemaker"
}
```

**cURL Example**:
```bash
curl -X POST https://api.resumecoach.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc123xyz",
    "job_title": "Software Engineer",
    "company_name": "TechCorp",
    "job_description": "..."
  }'
```

**Response** (200 OK):
```json
{
  "analysis": "# Resume Analysis for Software Engineer at TechCorp\n\n## Skills Match Score: 75%\n\n### ✅ Matching Skills:\n- Python (3+ years mentioned)\n- AWS (EC2, S3 experience)\n\n### ⚠️ Missing Skills:\n- FastAPI (not mentioned - add if you have experience)\n- Docker (mentioned briefly - elaborate)\n\n### 📝 Recommendations:\n1. Add dedicated 'Frameworks' section with FastAPI\n2. Quantify Python experience (e.g., '5 years')\n3. Expand AWS details (specific services)\n4. Add relevant projects\n\n### 💡 Interview Tips:\n- Prepare to discuss FastAPI vs Django\n- Review cloud architecture patterns\n- Study common Python design patterns",
  "match_score": 75,
  "missing_skills": ["FastAPI", "Docker containers"],
  "recommendations": [
    "Add FastAPI to skills section",
    "Quantify Python experience",
    "Expand AWS experience details"
  ]
}
```

**Errors**:
- `422`: Missing required fields
- `404`: Session not found
- `500`: Analysis error (LLM API issue)

---

### Interactive Chat

#### POST /api/chat

Ask questions about your resume and get AI-powered answers.

**Request**:
- Method: `POST`
- Content-Type: `application/json`
- Body:
```json
{
  "session_id": "abc123xyz",
  "message": "How can I better showcase my Python experience?",
  "provider": "openai"  // optional
}
```

**cURL Example**:
```bash
curl -X POST https://api.resumecoach.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc123xyz",
    "message": "How can I improve my resume?"
  }'
```

**Response** (200 OK):
```json
{
  "response": "To better showcase your Python experience:\n\n1. **Quantify your experience**: Instead of just listing Python, mention '5 years of Python development'\n\n2. **Highlight frameworks**: List specific frameworks like FastAPI, Django, Flask\n\n3. **Add metrics**: Include impact metrics (e.g., 'Built Python services handling 100K+ requests/day')\n\n4. **Show diversity**: Mention different areas (web dev, data processing, automation)\n\n5. **Include projects**: Link to GitHub projects demonstrating Python skills",
  "session_id": "abc123xyz"
}
```

**Errors**:
- `422`: Missing message or session_id
- `404`: Session not found
- `500`: Chat error

---

### LLM Provider Management

#### GET /api/llm-status

Get current LLM provider status.

**Response** (200 OK):
```json
{
  "provider": "openai",
  "model": "gpt-3.5-turbo",
  "available_providers": ["openai", "sagemaker"],
  "status": "operational"
}
```

---

#### POST /api/switch-provider

Switch between LLM providers.

**Request**:
```json
{
  "provider": "sagemaker"  // "openai" or "sagemaker"
}
```

**Response** (200 OK):
```json
{
  "message": "Switched to sagemaker provider",
  "provider": "sagemaker",
  "model": "meta-llama-2-7b"
}
```

**Errors**:
- `422`: Invalid provider name
- `500`: Provider initialization failed

---

## 📋 Request/Response Format

### Standard Request Headers

```http
Content-Type: application/json
Accept: application/json
```

### Standard Response Format

**Success Response**:
```json
{
  "data": { ... },
  "message": "Success message",
  "timestamp": "2026-01-08T12:00:00Z"
}
```

**Error Response**:
```json
{
  "detail": "Error description",
  "error_code": "ERROR_CODE",
  "timestamp": "2026-01-08T12:00:00Z"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid request format |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

---

## ⚠️ Error Handling

### Error Response Structure

```json
{
  "detail": "Session not found",
  "error_code": "SESSION_NOT_FOUND",
  "timestamp": "2026-01-08T12:00:00Z",
  "path": "/api/session/abc123",
  "request_id": "req_xyz789"
}
```

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `INVALID_FILE_FORMAT` | File is not PDF | Upload PDF file only |
| `FILE_TOO_LARGE` | File exceeds 10 MB | Reduce file size |
| `SESSION_NOT_FOUND` | Invalid session ID | Upload resume first |
| `EMPTY_JOB_DESCRIPTION` | Job description empty | Provide valid description |
| `LLM_API_ERROR` | LLM provider error | Retry or switch provider |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait and retry |

### Error Handling Example

```python
import requests

try:
    response = requests.post(
        "https://api.resumecoach.com/api/analyze",
        json={"session_id": "abc123", ...}
    )
    response.raise_for_status()
    data = response.json()
    
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Session not found. Please upload resume first.")
    elif e.response.status_code == 429:
        print("Rate limit exceeded. Please wait.")
    elif e.response.status_code == 500:
        print("Server error. Please try again later.")
    else:
        print(f"Error: {e.response.json()['detail']}")
        
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
```

---

## 🚦 Rate Limiting

### Current Limits

| Endpoint | Requests per Minute | Burst |
|----------|---------------------|-------|
| `/api/upload-resume` | 2 | 5 |
| `/api/analyze` | 2 | 5 |
| `/api/chat` | 5 | 10 |
| All other endpoints | 10 | 20 |

### Rate Limit Headers

```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 8
X-RateLimit-Reset: 1704715200
```

### Rate Limit Exceeded Response

```json
{
  "detail": "Rate limit exceeded. Please wait 60 seconds.",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60
}
```

---

## 💻 Code Examples

### Python Example

```python
import requests
from typing import Dict, Any

class ResumeCoachClient:
    def __init__(self, base_url: str = "https://api.resumecoach.com"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def upload_resume(self, pdf_path: str) -> Dict[str, Any]:
        """Upload resume PDF and get session ID."""
        with open(pdf_path, "rb") as f:
            files = {"file": f}
            response = self.session.post(
                f"{self.base_url}/api/upload-resume",
                files=files
            )
            response.raise_for_status()
            return response.json()
    
    def parse_job(self, job_description: str) -> Dict[str, Any]:
        """Parse job description."""
        response = self.session.post(
            f"{self.base_url}/api/parse-job",
            json={"job_description": job_description}
        )
        response.raise_for_status()
        return response.json()
    
    def analyze(self, session_id: str, job_title: str, 
                company: str, job_desc: str) -> Dict[str, Any]:
        """Generate analysis report."""
        response = self.session.post(
            f"{self.base_url}/api/analyze",
            json={
                "session_id": session_id,
                "job_title": job_title,
                "company_name": company,
                "job_description": job_desc
            }
        )
        response.raise_for_status()
        return response.json()
    
    def chat(self, session_id: str, message: str) -> Dict[str, Any]:
        """Chat with AI about resume."""
        response = self.session.post(
            f"{self.base_url}/api/chat",
            json={
                "session_id": session_id,
                "message": message
            }
        )
        response.raise_for_status()
        return response.json()

# Usage
client = ResumeCoachClient()

# Upload resume
result = client.upload_resume("resume.pdf")
session_id = result["session_id"]

# Parse job
job_data = client.parse_job("Software Engineer with Python...")

# Get analysis
analysis = client.analyze(
    session_id=session_id,
    job_title="Software Engineer",
    company="TechCorp",
    job_desc="Software Engineer with Python..."
)

print(analysis["analysis"])

# Ask questions
chat_response = client.chat(
    session_id=session_id,
    message="How can I improve my resume?"
)

print(chat_response["response"])
```

### JavaScript Example

```javascript
class ResumeCoachClient {
  constructor(baseUrl = 'https://api.resumecoach.com') {
    this.baseUrl = baseUrl;
  }

  async uploadResume(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/api/upload-resume`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return response.json();
  }

  async parseJob(jobDescription) {
    const response = await fetch(`${this.baseUrl}/api/parse-job`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ job_description: jobDescription })
    });

    if (!response.ok) {
      throw new Error(`Parse failed: ${response.statusText}`);
    }

    return response.json();
  }

  async analyze(sessionId, jobTitle, company, jobDescription) {
    const response = await fetch(`${this.baseUrl}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        job_title: jobTitle,
        company_name: company,
        job_description: jobDescription
      })
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }

    return response.json();
  }

  async chat(sessionId, message) {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        message: message
      })
    });

    if (!response.ok) {
      throw new Error(`Chat failed: ${response.statusText}`);
    }

    return response.json();
  }
}

// Usage
const client = new ResumeCoachClient();

// Upload resume
const fileInput = document.getElementById('resume-upload');
const result = await client.uploadResume(fileInput.files[0]);
const sessionId = result.session_id;

// Parse job
const jobData = await client.parseJob('Software Engineer with Python...');

// Get analysis
const analysis = await client.analyze(
  sessionId,
  'Software Engineer',
  'TechCorp',
  'Software Engineer with Python...'
);

console.log(analysis.analysis);
```

### cURL Examples

```bash
# Upload resume
curl -X POST https://api.resumecoach.com/api/upload-resume \
  -F "file=@resume.pdf"

# Parse job description
curl -X POST https://api.resumecoach.com/api/parse-job \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Software Engineer with 3+ years Python..."
  }'

# Generate analysis
curl -X POST https://api.resumecoach.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc123xyz",
    "job_title": "Software Engineer",
    "company_name": "TechCorp",
    "job_description": "Software Engineer with Python..."
  }'

# Chat
curl -X POST https://api.resumecoach.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "abc123xyz",
    "message": "How can I improve my resume?"
  }'

# Check health
curl https://api.resumecoach.com/api/health

# Get LLM status
curl https://api.resumecoach.com/api/llm-status

# Switch provider
curl -X POST https://api.resumecoach.com/api/switch-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "sagemaker"}'
```

---

## 📚 Additional Resources

- **Interactive API Docs**: https://api.resumecoach.com/docs
- **GitHub Repository**: https://github.com/mykh74/resumecoach
- **User Manual**: [USER_MANUAL.md](./USER_MANUAL.md)
- **Admin Guide**: [ADMIN_GUIDE.md](./ADMIN_GUIDE.md)
- **Support Email**: support@resumecoach.com

---

**Last Updated**: January 8, 2026  
**API Version**: 1.0  
**Status**: Production Ready
