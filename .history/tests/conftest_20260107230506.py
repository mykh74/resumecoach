"""
Test fixtures and utilities for Resume Coach tests.
"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing."""
    return """
    Jane Smith
    jane.smith@email.com | +1 (555) 987-6543
    linkedin.com/in/janesmith | github.com/janesmith
    San Francisco, CA
    
    PROFESSIONAL SUMMARY
    Results-driven Data Scientist with 6 years of experience in machine learning,
    statistical analysis, and data visualization. Proven track record of delivering
    actionable insights and building predictive models.
    
    TECHNICAL SKILLS
    Programming: Python, R, SQL, JavaScript
    ML/AI: TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy
    Tools: Git, Docker, Kubernetes, AWS (SageMaker, EC2, S3)
    Databases: PostgreSQL, MongoDB, Redis
    Visualization: Matplotlib, Seaborn, Plotly, Tableau
    
    PROFESSIONAL EXPERIENCE
    
    Senior Data Scientist
    DataTech Solutions Inc. | San Francisco, CA
    March 2021 - Present
    • Led development of recommendation system serving 5M+ users, increasing engagement by 35%
    • Built and deployed NLP models for sentiment analysis with 92% accuracy
    • Managed team of 3 data scientists and 2 ML engineers
    • Implemented MLOps pipeline reducing model deployment time by 60%
    • Presented insights to C-level executives and key stakeholders
    
    Data Scientist
    Analytics Corp | Mountain View, CA
    June 2018 - February 2021
    • Developed predictive models for customer churn, reducing attrition by 25%
    • Created automated data pipelines processing 10TB+ daily
    • Performed A/B testing and statistical analysis for product features
    • Collaborated with engineering teams on model integration
    
    Junior Data Analyst
    StartupXYZ | San Francisco, CA
    January 2017 - May 2018
    • Analyzed user behavior data to identify growth opportunities
    • Built dashboards and reports for business stakeholders
    • Conducted exploratory data analysis on large datasets
    
    EDUCATION
    
    Master of Science in Data Science
    University of California, Berkeley | Berkeley, CA
    Graduated: May 2016 | GPA: 3.9/4.0
    
    Bachelor of Science in Computer Science
    Stanford University | Stanford, CA
    Graduated: May 2014 | GPA: 3.7/4.0
    
    CERTIFICATIONS
    • AWS Certified Machine Learning - Specialty
    • TensorFlow Developer Certificate
    • Professional Scrum Master (PSM I)
    
    PROJECTS
    • Open-source contributor to Scikit-learn and Pandas libraries
    • Published research paper on deep learning in computer vision (500+ citations)
    
    AWARDS
    • "Data Scientist of the Year" - DataTech Solutions (2022)
    • Kaggle Competition Gold Medal - Image Classification Challenge
    """


@pytest.fixture
def sample_job_description():
    """Sample job description for testing."""
    return """
    Senior Machine Learning Engineer
    
    Company: AI Innovations Inc.
    Location: San Francisco, CA (Hybrid)
    Job Type: Full-time
    Experience Level: Senior (5-8 years)
    Salary: $150,000 - $200,000
    
    ABOUT THE COMPANY
    AI Innovations is a leading company in artificial intelligence and machine learning
    solutions. We work with Fortune 500 companies to build cutting-edge AI systems.
    
    ABOUT THE ROLE
    We're looking for a Senior Machine Learning Engineer to join our core ML team.
    You'll be responsible for designing and implementing production ML systems at scale.
    
    KEY RESPONSIBILITIES
    • Design, develop, and deploy machine learning models for production environments
    • Build scalable ML infrastructure and pipelines
    • Collaborate with data scientists to productionize research models
    • Optimize model performance and reduce latency
    • Mentor junior engineers and contribute to technical decisions
    • Lead projects from conception to deployment
    
    REQUIRED QUALIFICATIONS
    • 5+ years of experience in machine learning or related field
    • Strong programming skills in Python and experience with ML frameworks (TensorFlow, PyTorch)
    • Experience deploying ML models to production at scale
    • Solid understanding of ML algorithms, statistics, and mathematics
    • Experience with cloud platforms (AWS, GCP, or Azure)
    • Bachelor's or Master's degree in Computer Science, Math, or related field
    • Excellent communication and collaboration skills
    
    PREFERRED QUALIFICATIONS
    • PhD in Computer Science, Machine Learning, or related field
    • Experience with MLOps tools and practices
    • Knowledge of distributed computing frameworks (Spark, Ray)
    • Experience with deep learning and neural networks
    • Contributions to open-source ML projects
    • Published research in top-tier ML conferences
    • Experience with Kubernetes and Docker
    
    WHAT WE OFFER
    • Competitive salary and equity package
    • Comprehensive health, dental, and vision insurance
    • 401(k) matching
    • Flexible work arrangements (hybrid remote)
    • Professional development budget ($5,000/year)
    • Gym membership
    • Catered lunches and snacks
    • Collaborative and innovative work environment
    """


@pytest.fixture
def temp_pdf_path(tmp_path):
    """Create a temporary PDF path for testing."""
    return tmp_path / "test_resume.pdf"
