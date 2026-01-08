# Resume Coach - 2-Week Sprint Plan

**Timeline**: 14 Days  
**Start Date**: January 7, 2026  
**Deadline**: January 20, 2026

## 🎯 Project Goal
Build and deploy an AI-powered Resume Coach that analyzes resumes against job descriptions, provides coaching advice, and includes an interactive chatbot interface.

## 📋 MVP Feature Set

### Must-Have (Core):
- ✅ PDF resume upload and parsing
- ✅ Job description text input
- ✅ AI-generated coaching report (fit assessment, gaps, strengths, advice)
- ✅ Interactive chatbot for follow-up questions
- ✅ LLM hosted on AWS SageMaker
- ✅ Web app deployed on AWS EC2
- ✅ Complete documentation

### Nice-to-Have (If time permits):
- 🔄 Job posting database/search
- 🔄 Multiple resume formats (Word, TXT)
- 🔄 User authentication
- 🔄 Export reports as PDF

---

## 📅 Day-by-Day Breakdown

### **Days 1-2: Project Setup & Initial Prototyping** (Jan 7-8)

#### Day 1 - Setup & Architecture
**Time**: 8 hours

**Morning (4h)**:
- [ ] Initialize project repository structure
- [ ] Set up Python virtual environment
- [ ] Install core dependencies
- [ ] Configure AWS CLI and credentials
- [ ] Create development environment checklist

**Afternoon (4h)**:
- [ ] Quick EDA on sample job postings (use Kaggle dataset)
- [ ] Collect 5-10 test resumes (anonymized)
- [ ] Create initial system architecture diagram
- [ ] Set up Jupyter notebook for experiments

**Project Structure**:
```
ResumeCoach/
├── backend/
│   ├── api/              # Flask/FastAPI endpoints
│   ├── services/         # LLM orchestration, resume parsing
│   ├── models/           # Data models
│   ├── prompts/          # Prompt templates
│   └── utils/            # Helper functions
├── frontend/
│   └── streamlit_app.py  # Streamlit application
├── notebooks/            # Jupyter experiments
├── data/
│   ├── sample_resumes/
│   └── job_postings/
├── deployment/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── docs/                 # All documentation
├── tests/
├── requirements.txt
└── README.md
```

**Dependencies to install**:
```bash
# Core
langchain==0.1.0
langchain-community==0.0.10
openai==1.6.1
anthropic==0.8.1

# PDF Processing
PyPDF2==3.0.1
pdfplumber==0.10.3
python-docx==1.1.0

# Backend
fastapi==0.109.0
uvicorn==0.25.0
pydantic==2.5.3

# Frontend
streamlit==1.29.0

# AWS
boto3==1.34.22
sagemaker==2.199.0

# ML/AI
transformers==4.36.2
torch==2.1.2
sentence-transformers==2.2.2

# Utilities
python-dotenv==1.0.0
requests==2.31.0
```

#### Day 2 - Initial LLM Testing
**Time**: 8 hours

**Morning (4h)**:
- [ ] Sign up for OpenAI API (for initial testing)
- [ ] Sign up for Replicate (Llama-2 hosted API)
- [ ] Create basic LangChain chain with GPT-3.5
- [ ] Test with 2-3 resume/job combinations
- [ ] Document initial findings

**Afternoon (4h)**:
- [ ] Design initial prompt templates (5 types of advice)
- [ ] Test prompts with different models
- [ ] Create prompt evaluation notebook
- [ ] Refine prompts based on outputs
- [ ] Document best-performing prompts

**Deliverables**:
- ✅ Working project structure
- ✅ Initial prompt templates
- ✅ Sample data collected
- ✅ Basic LLM integration working

---

### **Days 3-4: Prompt Engineering & Resume Parser** (Jan 9-10)

#### Day 3 - Resume Parser Development
**Time**: 8 hours

**Morning (4h)**:
- [ ] Build PDF resume parser
  - Extract text from PDF
  - Structure extraction (sections: experience, education, skills)
  - Handle different resume formats
- [ ] Test parser with 10+ sample resumes
- [ ] Create parser test suite

**Afternoon (4h)**:
- [ ] Build job description parser
  - Extract key requirements
  - Identify must-have vs nice-to-have skills
  - Extract company/role information
- [ ] Create unified data model for parsed data
- [ ] Write unit tests

**Code Structure**:
```python
# backend/services/resume_parser.py
class ResumeParser:
    def parse_pdf(self, file_path) -> dict
    def extract_sections(self, text) -> dict
    def extract_skills(self, text) -> list
    
# backend/services/job_parser.py
class JobParser:
    def parse_job_description(self, text) -> dict
    def extract_requirements(self, text) -> dict
```

#### Day 4 - Advanced Prompt Engineering
**Time**: 8 hours

**Morning (4h)**:
- [ ] Design multi-step coaching workflow:
  1. Analyze job requirements
  2. Analyze resume qualifications
  3. Compare and identify gaps
  4. Generate strengths
  5. Provide actionable advice
- [ ] Implement chain-of-thought prompting
- [ ] Test with 20+ combinations

**Afternoon (4h)**:
- [ ] Build chatbot conversation system
  - Conversation memory management
  - Context handling for long documents
  - Follow-up question handling
- [ ] Create prompt library (10+ templates)
- [ ] Document prompt engineering decisions

**Deliverables**:
- ✅ Working resume parser (PDF)
- ✅ Job description analyzer
- ✅ Refined prompt templates
- ✅ Chatbot conversation flow

---

### **Days 5-6: Backend API & LLM Integration** (Jan 11-12)

#### Day 5 - Backend API Development
**Time**: 8 hours

**Morning (4h)**:
- [ ] Set up FastAPI project structure
- [ ] Create API endpoints:
  - `POST /api/upload-resume` - Upload and parse
  - `POST /api/analyze` - Generate coaching report
  - `POST /api/chat` - Chatbot interaction
  - `GET /api/health` - Health check
- [ ] Implement request/response models with Pydantic

**Afternoon (4h)**:
- [ ] Add file upload handling (multipart/form-data)
- [ ] Implement error handling and validation
- [ ] Add logging and monitoring
- [ ] Create API documentation (OpenAPI/Swagger)
- [ ] Test endpoints with Postman/curl

**API Design**:
```python
# POST /api/analyze
{
  "resume_text": "...",
  "job_description": "...",
  "analysis_type": ["fit", "gaps", "strengths", "advice"]
}

# Response
{
  "coaching_report": {
    "fit_score": 8.5,
    "overall_assessment": "...",
    "gaps": [...],
    "strengths": [...],
    "advice": [...]
  },
  "session_id": "uuid"
}

# POST /api/chat
{
  "session_id": "uuid",
  "message": "How can I improve my technical skills section?"
}
```

#### Day 6 - LangChain Integration
**Time**: 8 hours

**Morning (4h)**:
- [ ] Build LangChain orchestration layer
  - Create custom chains for each advice type
  - Implement prompt templates with LangChain
  - Add conversation memory (ConversationBufferMemory)
- [ ] Integrate with OpenAI API (temporary)
- [ ] Test complete analysis workflow

**Afternoon (4h)**:
- [ ] Add caching layer (reduce API costs)
- [ ] Implement rate limiting
- [ ] Add async processing for long operations
- [ ] Create abstraction for LLM providers
  - Easy switching between OpenAI, Replicate, SageMaker
- [ ] Integration tests

**Deliverables**:
- ✅ Working FastAPI backend
- ✅ LangChain integration complete
- ✅ All API endpoints functional
- ✅ Ready for frontend integration

---

### **Days 7-8: Streamlit Frontend Development** (Jan 13-14)

#### Day 7 - Core UI Components
**Time**: 8 hours

**Morning (4h)**:
- [ ] Create Streamlit app structure
- [ ] Build landing page with instructions
- [ ] Implement file uploader for resume (PDF)
- [ ] Create text area for job description input
- [ ] Add "Analyze" button and loading state

**Afternoon (4h)**:
- [ ] Display coaching report in formatted sections:
  - Overall fit assessment (with score visualization)
  - Gaps analysis (list with icons)
  - Strengths to highlight (highlighted boxes)
  - General advice (actionable items)
- [ ] Add styling with custom CSS
- [ ] Implement responsive design

**Streamlit Structure**:
```python
# frontend/streamlit_app.py
import streamlit as st

def main():
    st.set_page_config(page_title="Resume Coach", layout="wide")
    
    # Sidebar
    with st.sidebar:
        - About section
        - Settings (model parameters)
        - Clear history button
    
    # Main content
    tabs = st.tabs(["Analyze", "Chat", "Help"])
    
    with tabs[0]:  # Analyze
        - Resume upload
        - Job description input
        - Analyze button
        - Results display
    
    with tabs[1]:  # Chat
        - Chat interface
        - Conversation history
    
    with tabs[2]:  # Help
        - Usage instructions
        - Examples
```

#### Day 8 - Chatbot Interface & Polish
**Time**: 8 hours

**Morning (4h)**:
- [ ] Build chat interface with st.chat_message
- [ ] Implement conversation history display
- [ ] Add message input and send functionality
- [ ] Connect to backend chat API
- [ ] Show typing indicators

**Afternoon (4h)**:
- [ ] Add advanced features:
  - Download report as text
  - Sample resume/job examples
  - Model parameter tuning (temperature, max tokens)
- [ ] Error handling and user feedback
- [ ] Loading states and progress indicators
- [ ] Final UI polish and testing

**Deliverables**:
- ✅ Complete Streamlit application
- ✅ Resume upload and analysis working
- ✅ Chatbot interface functional
- ✅ End-to-end testing complete

---

### **Days 9-10: AWS SageMaker Deployment** (Jan 15-16)

#### Day 9 - SageMaker Setup & Model Selection
**Time**: 8 hours

**Morning (4h)**:
- [ ] Review AWS credits and budget
- [ ] Research SageMaker instance types and costs
- [ ] Decision: Choose model size
  - **Recommended**: Llama-2-7B-chat (fits ml.g5.xlarge)
  - Alternative: Llama-2-13B-chat (needs ml.g5.2xlarge)
- [ ] Test Llama-2 locally with quantization first (4-bit)

**Afternoon (4h)**:
- [ ] Deploy Llama-2 via SageMaker JumpStart:
  1. Open SageMaker Studio
  2. Navigate to JumpStart
  3. Search "Llama-2-7B-chat"
  4. Click Deploy
  5. Choose instance type: ml.g5.xlarge
  6. Deploy and wait (~15 minutes)
- [ ] Test endpoint with sample inputs
- [ ] Document endpoint configuration

**SageMaker Deployment Steps**:
```python
# Alternative: Deploy with Boto3
import boto3
import sagemaker
from sagemaker.huggingface import HuggingFaceModel

# Define model
huggingface_model = HuggingFaceModel(
    model_data="s3://path-to-model-or-hf-model-id",
    role=sagemaker.get_execution_role(),
    transformers_version="4.26",
    pytorch_version="1.13",
    py_version="py39",
)

# Deploy
predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type="ml.g5.xlarge",
)
```

#### Day 10 - Backend Integration with SageMaker
**Time**: 8 hours

**Morning (4h)**:
- [ ] Create SageMaker client in backend
- [ ] Implement SageMaker LLM provider class
- [ ] Update LangChain to use SageMaker endpoint
- [ ] Test full pipeline with SageMaker
- [ ] Compare outputs with OpenAI baseline

**Afternoon (4h)**:
- [ ] Optimize inference parameters:
  - Temperature: 0.7
  - Max tokens: 1024
  - Top-p: 0.9
- [ ] Add retry logic and error handling
- [ ] Monitor token usage and costs
- [ ] Performance testing and optimization
- [ ] Document SageMaker integration

**Code Example**:
```python
# backend/services/sagemaker_llm.py
import boto3
import json

class SageMakerLLM:
    def __init__(self, endpoint_name):
        self.client = boto3.client('sagemaker-runtime')
        self.endpoint_name = endpoint_name
    
    def generate(self, prompt, max_tokens=1024):
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        response = self.client.invoke_endpoint(
            EndpointName=self.endpoint_name,
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        
        result = json.loads(response['Body'].read())
        return result[0]['generated_text']
```

**Deliverables**:
- ✅ Llama-2 deployed on SageMaker
- ✅ Backend integrated with SageMaker
- ✅ Full pipeline working end-to-end
- ✅ Performance optimized

---

### **Days 11-12: Integration & Testing** (Jan 17-18)

#### Day 11 - Full Integration Testing
**Time**: 8 hours

**Morning (4h)**:
- [ ] Connect frontend to backend with SageMaker
- [ ] Test complete user flows:
  1. Upload resume → Parse → Analyze → View report
  2. Start chat → Ask questions → Get responses
  3. Try different resumes and job descriptions
- [ ] Fix integration bugs
- [ ] Test error scenarios

**Afternoon (4h)**:
- [ ] Performance testing:
  - Measure response times
  - Test with large resumes (10+ pages)
  - Test with long job descriptions
  - Concurrent user simulation
- [ ] Optimize bottlenecks
- [ ] Add caching where appropriate

#### Day 12 - Quality Assurance & Fine-tuning Docs
**Time**: 8 hours

**Morning (4h)**:
- [ ] Test with 20+ real resume/job combinations
- [ ] Evaluate output quality:
  - Accuracy of gap analysis
  - Relevance of advice
  - Chatbot response quality
- [ ] Refine prompts based on results
- [ ] Edge case testing

**Afternoon (4h)**:
- [ ] Prepare fine-tuning documentation:
  - Create sample fine-tuning dataset format
  - Document LoRA/QLoRA fine-tuning process
  - Provide fine-tuning code example
  - Store in `docs/FINE_TUNING.md`
- [ ] Create test suite
- [ ] Document known limitations

**Fine-tuning Dataset Format**:
```json
{
  "instruction": "Analyze this resume against the job description and provide coaching advice.",
  "input": {
    "resume": "...",
    "job_description": "..."
  },
  "output": "Your resume shows strong qualifications for this role. You have 8 years of experience in software engineering which exceeds the 5+ years requirement..."
}
```

**Deliverables**:
- ✅ Fully integrated and tested system
- ✅ Performance optimized
- ✅ Fine-tuning documentation complete
- ✅ Test suite ready

---

### **Days 13-14: AWS Deployment & Documentation** (Jan 19-20)

#### Day 13 - AWS EC2 Deployment
**Time**: 8 hours

**Morning (4h)**:
- [ ] Create Dockerfiles for backend and frontend
- [ ] Build Docker images locally and test
- [ ] Create docker-compose.yml for orchestration
- [ ] Push images to Docker Hub or AWS ECR

**Docker Setup**:
```dockerfile
# deployment/Dockerfile.backend
FROM python:3.10-slim
WORKDIR /app
COPY backend/ /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# deployment/Dockerfile.frontend
FROM python:3.10-slim
WORKDIR /app
COPY frontend/ /app/
RUN pip install streamlit
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501"]
```

**Afternoon (4h)**:
- [ ] Launch EC2 instance:
  - Type: t3.medium (2 vCPU, 4GB RAM)
  - OS: Ubuntu 22.04 LTS
  - Storage: 30GB
  - Security group: Open ports 80, 443, 8501, 8000
- [ ] SSH into instance
- [ ] Install Docker and Docker Compose
- [ ] Clone repository
- [ ] Deploy containers
- [ ] Configure nginx reverse proxy
- [ ] Set up SSL with Let's Encrypt (optional)

**EC2 Setup Commands**:
```bash
# SSH into EC2
ssh -i key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# Install Docker
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker ubuntu

# Deploy
git clone <your-repo>
cd ResumeCoach/deployment
docker-compose up -d

# Check status
docker ps
docker logs backend
docker logs frontend
```

#### Day 14 - Documentation & Final Polish
**Time**: 8 hours

**Morning (4h)**:
- [ ] Complete all documentation files:
  - `README.md` - Project overview, quick start
  - `docs/ARCHITECTURE.md` - System design, diagrams
  - `docs/DEPLOYMENT.md` - Step-by-step AWS setup
  - `docs/API_DOCUMENTATION.md` - API endpoints
  - `docs/PROMPTS.md` - All prompt templates
  - `docs/USER_MANUAL.md` - How to use the app
  - `docs/FINE_TUNING.md` - Fine-tuning guide
- [ ] Create architecture diagrams
- [ ] Take screenshots of deployment

**Afternoon (4h)**:
- [ ] Record demo video (5-10 minutes):
  1. Show application homepage
  2. Upload sample resume
  3. Enter job description
  4. Show coaching report
  5. Demonstrate chatbot
  6. Show deployment on AWS
- [ ] Final testing on production
- [ ] Create submission package
- [ ] Cost analysis and report

**Documentation Checklist**:
- ✅ README with badges and overview
- ✅ Architecture diagram with AWS services
- ✅ Complete deployment guide
- ✅ API documentation with examples
- ✅ Prompt engineering documentation
- ✅ User manual with screenshots
- ✅ Fine-tuning documentation
- ✅ Troubleshooting guide
- ✅ Cost breakdown and optimization tips

**Deliverables**:
- ✅ Application deployed on AWS
- ✅ Complete documentation package
- ✅ Demo video recorded
- ✅ Project ready for submission

---

## 🎯 Critical Success Factors

### Week 1 Priorities:
1. **Get LLM working** (OpenAI/Replicate) - Don't wait for SageMaker
2. **Nail prompt engineering** - This is 25% of your grade
3. **Build solid resume parser** - Core functionality
4. **Create working prototype** - Frontend + Backend integrated

### Week 2 Priorities:
1. **Deploy to SageMaker** - Must-have for grading
2. **Deploy to AWS EC2** - Required deliverable
3. **Complete documentation** - 5% of grade but critical
4. **Polish and test** - Ensure it works flawlessly

---

## 💰 Budget Management (AWS Credits)

### Cost Estimates:
- **SageMaker ml.g5.xlarge**: ~$1.50/hour
  - 5 days × 8 hours = 40 hours = **$60**
- **EC2 t3.medium**: ~$0.05/hour
  - 14 days × 24 hours = 336 hours = **$17**
- **S3, Data Transfer**: ~**$5**
- **Total**: ~**$82** (conservative estimate)

### Optimization:
- ⚠️ **STOP SageMaker endpoint when not actively testing**
- ⚠️ Use Replicate API during development ($0.00015/token)
- Only deploy to SageMaker on Day 9
- Use smallest instance types
- Monitor with AWS Cost Explorer daily

---

## 🔧 Tools & Technologies

### Core Stack:
- **Language**: Python 3.10+
- **LLM Framework**: LangChain
- **LLM Model**: Llama-2-7B-chat (SageMaker)
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Cloud**: AWS (SageMaker, EC2, S3)
- **Containerization**: Docker
- **Version Control**: Git

### Development Tools:
- Jupyter Notebook (experimentation)
- Postman (API testing)
- VS Code (IDE)
- AWS CLI
- Docker Desktop

---

## 📊 Daily Progress Tracking

Create a simple daily log:

```markdown
# Day 1 - Jan 7
- ✅ Project setup complete
- ✅ Dependencies installed
- ✅ Initial EDA done
- 🔄 Prompt testing in progress
- ⚠️ Issue: PDF parser needs more work

# Day 2 - Jan 8
...
```

---

## 🚨 Risk Mitigation

### High-Risk Items:
1. **SageMaker deployment fails**: 
   - Mitigation: Keep OpenAI/Replicate as backup
   - Can still score well with hosted API + deployment docs

2. **AWS credits run out**:
   - Mitigation: Monitor daily, stop instances when not in use
   - Use free tier services where possible

3. **Prompt engineering takes too long**:
   - Mitigation: Start with simple prompts, iterate
   - Focus on quality over quantity

4. **Integration issues**:
   - Mitigation: Test components independently first
   - Build modular architecture

---

## ✅ Pre-Submission Checklist

### Code:
- [ ] All code is clean and well-commented
- [ ] No hardcoded credentials (use .env)
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Tests written and passing

### Deployment:
- [ ] Application accessible via public URL
- [ ] SageMaker endpoint working
- [ ] All services running on AWS
- [ ] SSL configured (optional but nice)

### Documentation:
- [ ] README is comprehensive
- [ ] Architecture diagram included
- [ ] Deployment guide is step-by-step
- [ ] All prompts documented
- [ ] API docs complete
- [ ] Screenshots/video included
- [ ] Fine-tuning code provided

### Testing:
- [ ] Tested with 10+ resume/job combinations
- [ ] Chatbot works correctly
- [ ] Error cases handled gracefully
- [ ] Performance is acceptable (<10s response time)

---

## 📞 Getting Help

If you get stuck:
1. Check AWS documentation
2. LangChain documentation
3. Stack Overflow
4. AWS Support (if credits issue)
5. Course instructors/TAs

---

## 🎓 Grading Alignment

| Criteria | Weight | Your Focus |
|----------|--------|------------|
| EDA & Data Prep | 5% | Day 1-2: Job posting analysis |
| Hyperparameter Tuning | 5% | Day 12: Fine-tuning docs |
| Model Deployment | 25% | Days 9-10, 13: SageMaker + EC2 |
| Web Application | 25% | Days 7-8: Streamlit with all features |
| Creativity | 10% | Days 3-4: PDF parsing, context handling |
| Prompt Engineering | 25% | Days 2-4: Multiple strategies, refinement |
| Documentation | 5% | Day 14: Complete docs package |

---

**Good luck! Stay focused on the MVP and ship early, iterate often.**
