# Resume Coach 🎯

An AI-powered career coaching application that analyzes resumes against job descriptions and provides personalized guidance through intelligent coaching reports and interactive chat.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)](https://streamlit.io/)
[![AWS](https://img.shields.io/badge/AWS-SageMaker-orange.svg)](https://aws.amazon.com/sagemaker/)

## 🌟 Features

- **📄 Resume Analysis**: Upload your resume (PDF) and get instant AI-powered analysis
- **🎯 Job Matching**: Compare your qualifications against specific job descriptions
- **💡 Smart Coaching**: Receive personalized advice on:
  - Overall fit assessment with scoring
  - Gap analysis (missing qualifications)
  - Strengths to highlight in applications
  - Actionable improvement recommendations
- **💬 Interactive Chatbot**: Ask follow-up questions and get career coaching in real-time
- **🤖 Multi-Provider LLM Support**: 
  - OpenAI (GPT-3.5/4) - Easy setup, great for testing
  - AWS SageMaker (Llama 2, Mistral, Falcon) - Privacy, cost control, production scale
- **☁️ AWS SageMaker Integration**: Self-hosted LLMs for data privacy and performance

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────────────────┐
│  Streamlit  │─────▶│   FastAPI    │─────▶│     LLM Service             │
│  Frontend   │      │   Backend    │      │  (Multi-Provider Support)   │
│  (4 pages)  │      │ (10 endpoints)│      └─────────────────────────────┘
└─────────────┘      └──────────────┘                    │
                            │                            ├─▶ OpenAI API
                            ▼                            │   (GPT-3.5/4)
                     ┌──────────────┐                   │
                     │  LangChain   │                   └─▶ AWS SageMaker
                     │ Orchestration│                       (Llama 2, Mistral)
                     └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- **For OpenAI (easiest):** OpenAI API key
- **For SageMaker (optional):** AWS account with IAM credentials
  - See [docs/AWS_SETUP_GUIDE.md](docs/AWS_SETUP_GUIDE.md) for setup instructions

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ResumeCoach
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .envcredentials:
   # - OPENAI_API_KEY=your_key (required)
   # - For SageMaker: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc. (optional)
   # Edit .env with your API keys
   ```

5. **Run the backend**:
   ```bash
   cd backend
   uvicorn api.main:app --reload
   ```

6. **Run the frontend** (in a new terminal):
   ```bash
   cd frontend
   streamlit run streamlit_app.py
   ```

### 🚀 One-Command Launch

Run both backend and frontend together:
```bash
./run_app.sh
```

### ☁️ AWS SageMaker Deplo    # FastAPI endpoints (10 endpoints)
│   │   └── main.py
│   ├── services/             # Business logic
│   │   ├── resume_parser.py  # PDF resume parsing
│   │   ├── job_parser.py     # Job description parsing
│   │   └── llm_service.py    # Multi-provider LLM orchestration
│   ├── models/               # Data models (Pydantic)
│   │   └── schema.py
│   ├── prompts/              # Prompt templates
│   │   └── templates.py
│   └── utils/                # Helper functions
├── frontend/
│   ├── streamlit_app.py      # Main app entry
│   └── pages/                # Streamlit pages (4 pages)
│       ├── upload_page.py
│       ├── analysis_page.py
│       └── chat_page.py
├── aws/                      # AWS SageMaker integration
│   ├── sagemaker_deployer.py # Model deployment
│   └── sagemaker_client.py   # Inference client
├── scripts/                  # Automation scripts
│   └── compare_providers.py  # OpenAI vs SageMaker comparison
├── docs/                     # Documentation
│   ├── AWS_SETUP_GUIDE.md
│   ├── SAGEMAKER_QUICK_REFERENCE.md
│   ├── DAY9-10_SAGEMAKER_DEPLOYMENT.md
│   ├── DAY7-8_REPORT.md
│   ├── FRONTEND.md
│   └── E2E_TEST_REPORT.md
├── tests/
│   ├── test_parsers.py       # Parser tests (15 passing)
│   ├── test_api.py           # API tests (7 passing)
│   └── test_e2e.py           # E2E tests (7 passing)
├── deploy_sagemaker.py       # SageMaker deployment CLI
├── run_app.sh                # One-command launcher
│   │   └── chat_service.py
│   ├── models/           # Data models
│   │   ├── resume.py
│   │   └── coaching.py
│   ├── prompts/          # Prompt templates
│   │   └── templates.py
│   └── utils/            # Helper functions
├── frontend/
│   └── streamlit_app.py  # Streamlit UI
├── notebooks/            # Jupyter experiments
│   ├── eda.ipynb
│   └── prompt_testing.ipynb
├── data/
│   ├── sample_resumes/
│   └── job_postings/
├── deployment/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── docs/                 # Documentation
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── API_DOCUMENTATION.md
│   ├── PROMPTS.md
│   ├── USER_MANUAL.md
│   └── FINE_TUNING.md
├── tests/               # Unit tests
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 📊 Development Status
**Current Phase:** Days 13-14 - AWS Deployment & Documentation ✅ COMPLETE

### Completed Milestones

- ✅ **Days 1-2:** Project Setup & Prototyping
- ✅ **Days 3-4:** Resume Parser & Prompt Engineering (15/15 tests passing)
- ✅ **Days 5-6:** FastAPI Backend (10 endpoints, 7/7 API tests passing)
- ✅ **Days 7-8:** Streamlit Frontend (4 pages, 7/7 E2E tests passing)
- ✅ **Days 9-10:** AWS SageMaker Deployment (Multi-provider support)
- ✅ **Days 11-12:** Integration & Testing (54/54 tests, load testing, benchmarks)
- ✅ **Days 13-14:** AWS Deployment & Final Documentation (Production ready!)

### Project Status

- **Progress**: 100% complete (14/14 days)
- **Completion Date**: January 8, 2026 (12 days ahead of schedule!)
- **Status**: 🟢 PRODUCTION READY 🚀

## 🛠️ Technology Stack

- **Models**: 
  - OpenAI GPT-3.5-turbo (default)
  - AWS SageMaker: Llama 2 7B/13B, Mistral 7B, Falcon 7B (optional)
- **Backend**: FastAPI 0.109.0, Python 3.13.1
- **Frontend**: Streamlit 1.29.0
- **Cloud**: AWS (SageMaker, EC2/ECS)
- **Testing**: Pytest, Locust (54/54 tests passing)
- **Infrastructure**: boto3, sagemaker SDK, locust
- **LLM Framework**: LangChain

## 📖 Documentation

### Getting Started
- [AWS Setup Guide](docs/AWS_SETUP_GUIDE.md) - How to get AWS credentials
- [SageMaker Quick Reference](docs/SAGEMAKER_QUICK_REFERENCE.md) - Common commands

### User & Admin Guides (NEW)
- 📖 [User Manual](docs/USER_MANUAL.md) - Complete end-user guide
- 🔧 [Admin Guide](docs/ADMIN_GUIDE.md) - System administration and operations
- 📡 [API Documentation](docs/API_DOCUMENTATION.md) - Complete API reference with examples
- 🚀 [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Step-by-step AWS deployment

### Implementation Details
- [Days 13-14 Deployment Plan](docs/DAY13-14_DEPLOYMENT_PLAN.md) - AWS deployment strategy (NEW)
- [Days 11-12 Test Report](docs/DAY11-12_TEST_REPORT.md) - Integration testing results
- [Days 11-12 Test Plan](docs/DAY11-12_TEST_PLAN.md) - Testing strategy
- [Days 9-10 Report](docs/DAY9-10_SAGEMAKER_DEPLOYMENT.md) - SageMaker deployment guide
- [Days 7-8 Report](docs/DAY7-8_REPORT.md) - Frontend development
- [Frontend Documentation](docs/FRONTEND.md) - Streamlit app architecture
- [E2E Test Report](docs/E2E_TEST_REPORT.md) - Testing results

### Final Documentation
- 🎯 [Final Project Summary](docs/FINAL_SUMMARY.md) - Complete project overview and handoff (NEW)
Comprehensive documentation is available in the `docs/` directory:

### Unit & Integration Tests

```bash
# Run all tests (29 tests)
pytest tests/

# Run specific test suites
pytest tests/test_parsers.py    # Parser tests (15 passing)
pytest tests/test_api.py         # API tests (7 passing)
pytest tests/test_e2e.py         # E2E tests (7 passing)

# Run with coverage
pytest --cov=backend tests/
```

### E2E Testing
Local Development

```bash
# Quick start - runs both backend and frontend
./run_app.sh
```

### AWS SageMaker Deployment

```bash
# 1. Set up AWS credentials (see docs/AWS_SETUP_GUIDE.md)

# 2. Deploy LLM model to SageMaker
python deploy_sagemaker.py --model mistral-7b-instruct

# 3. Update .env with endpoint name
echo "SAGEMAKER_ENDPOINT_NAME=resumecoach-mistral-7b-instruct" >> .env

# 4. Test deployment
python aws/sagemaker_client.py
```

See [docs/DAY9-10_SAGEMAKER_DEPLOYMENT.md](docs/DAY9-10_SAGEMAKER_DEPLOYMENT.md) for complete deployment guide.

### Production Deployment (Days 13-14 - Next)

- Backend: AWS ECS/EC2 or AWS Lambda
- Frontend: Streamlit Cloud or AWS
- Database: PostgreSQL for session storage
- Monitoring: CloudWatch logs and metrics

---

## 🧪 Testing

**Current Test Status:** ✅ 54/54 tests passing (100%)

### Test Suite Breakdown

| Test Type | Count | Status | Coverage |
|-----------|-------|--------|----------|
| Unit Tests | 22 | ✅ All passing | Parsers |
| API Tests | 7 | ✅ All passing | Endpoints |
| Integration Tests | 18 | ✅ All passing | Workflows |
| E2E Tests | 7 | ✅ All passing | Full app |
| **TOTAL** | **54** | ✅ **100%** | **Complete** |

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/test_integration.py -v

# Run with coverage
pytest --cov=backend tests/

# Run with timing
pytest tests/ -v --durations=10
```

### Load Testing

```bash
# Quick load test (10 users, 60s)
locust -f locustfile.py --headless -u 10 -r 2 -t 60s

# With HTML report
locust -f locustfile.py --headless -u 10 -r 2 -t 60s --html=reports/load_test.html

# Interactive web UI
locust -f locustfile.py
# Open http://localhost:8089
```

### Performance Benchmarking

```bash
# Run benchmarks
python scripts/benchmark_performance.py

# Create baseline
python scripts/benchmark_performance.py --create-baseline

# Compare with baseline
python scripts/benchmark_performance.py --compare results/baseline.json
```

## 🚢 Deployment

### Docker Deployment

```bash
docker-compose up -d
```

### AWS Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed AWS deployment instructions including:
- SageMaker model deployment
- EC2 instance setup
- Domain configuration
- SSL setup

## 📝 License

This project is developed as part of a machine learning course project.

## 👥 Contributors

- Michael Kuzmyn

## 🙏 Acknowledgments

- Built using Meta's Llama-2 model
- Powered by LangChain framework
- Hosted on AWS infrastructure

---

**Status**: 🚧 In Active Development

**Timeline**: 2-week sprint (Jan 7 - Jan 20, 2026)
