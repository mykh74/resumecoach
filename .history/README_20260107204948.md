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
- **🤖 Powered by Llama-2**: Self-hosted on AWS SageMaker for privacy and performance

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│  Streamlit  │─────▶│   FastAPI    │─────▶│   AWS SageMaker │
│   Frontend  │      │   Backend    │      │   (Llama-2-7B)  │
└─────────────┘      └──────────────┘      └─────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  LangChain   │
                     │ Orchestration│
                     └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- AWS account with credits
- OpenAI API key (for initial testing)

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
   cp .env.example .env
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

Visit `http://localhost:8501` to use the application!

## 📁 Project Structure

```
ResumeCoach/
├── backend/
│   ├── api/              # FastAPI endpoints
│   │   ├── main.py
│   │   └── routes/
│   ├── services/         # Business logic
│   │   ├── resume_parser.py
│   │   ├── job_parser.py
│   │   ├── llm_service.py
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

Current phase: **Day 1 - Project Setup** ✅

- [x] Git repository initialized
- [x] Project structure created
- [x] Dependencies defined
- [ ] Virtual environment setup
- [ ] Initial EDA
- [ ] Prompt testing

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the complete 14-day development roadmap.

## 🛠️ Technology Stack

- **LLM Framework**: LangChain
- **Models**: Llama-2-7B-chat (SageMaker), GPT-3.5/4 (testing)
- **Backend**: FastAPI, Python 3.10+
- **Frontend**: Streamlit
- **Cloud**: AWS (SageMaker, EC2, S3)
- **Containerization**: Docker
- **Testing**: Pytest

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Architecture Overview](docs/ARCHITECTURE.md) - System design and components
- [Deployment Guide](docs/DEPLOYMENT.md) - AWS deployment instructions
- [API Documentation](docs/API_DOCUMENTATION.md) - API endpoints and usage
- [User Manual](docs/USER_MANUAL.md) - End-user guide
- [Prompt Engineering](docs/PROMPTS.md) - Prompt templates and strategies
- [Fine-tuning Guide](docs/FINE_TUNING.md) - Model fine-tuning instructions

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=backend tests/
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
