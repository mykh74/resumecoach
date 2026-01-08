"""
Development Environment Setup Checklist
Complete this checklist to ensure your development environment is properly configured.
"""

# Development Environment Setup Checklist

## Day 1 - Initial Setup

### Git & Repository
- [x] Initialize git repository
- [x] Create .gitignore
- [x] Create project structure
- [ ] Create initial commit
- [ ] (Optional) Push to GitHub

### Python Environment
- [ ] Python 3.10+ installed (check: `python --version`)
- [ ] Create virtual environment (`python -m venv venv`)
- [ ] Activate virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Verify installation (`pip list`)

### API Keys & Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Sign up for OpenAI API (https://platform.openai.com/)
- [ ] Get OpenAI API key and add to `.env`
- [ ] (Optional) Sign up for Replicate (https://replicate.com/)
- [ ] (Optional) Get Replicate token and add to `.env`
- [ ] Test API connection

### AWS Setup
- [ ] AWS account created
- [ ] Check AWS credits balance
- [ ] Install AWS CLI (`pip install awscli` or via package manager)
- [ ] Configure AWS CLI (`aws configure`)
- [ ] Set AWS credentials in `.env`
- [ ] Verify AWS access (`aws sts get-caller-identity`)

### Development Tools
- [ ] VS Code (or preferred IDE) installed
- [ ] Python extension for VS Code installed
- [ ] Jupyter extension for VS Code installed (for notebooks)
- [ ] Postman or similar API testing tool installed
- [ ] Docker Desktop installed (for later deployment)

### Data Collection
- [ ] Download sample job postings dataset from Kaggle
  - Suggested: "LinkedIn Job Postings" or "Indeed Job Postings"
  - Place in `data/job_postings/`
- [ ] Collect 5-10 sample resumes (anonymized)
  - Place in `data/sample_resumes/`
  - PDF format preferred
- [ ] Verify data files are accessible

### Initial Testing
- [ ] Create test Jupyter notebook in `notebooks/`
- [ ] Test OpenAI API connection
- [ ] Test basic PDF parsing with PyPDF2
- [ ] Verify all imports work correctly

## Verification Commands

Run these commands to verify your setup:

```bash
# Check Python version
python --version  # Should be 3.10+

# Check virtual environment is activated
which python  # Should point to venv/bin/python

# Verify key packages
python -c "import openai; print(openai.__version__)"
python -c "import langchain; print(langchain.__version__)"
python -c "import fastapi; print(fastapi.__version__)"
python -c "import streamlit; print(streamlit.__version__)"

# Check AWS configuration
aws sts get-caller-identity

# Test environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenAI key configured:', bool(os.getenv('OPENAI_API_KEY')))"
```

## Common Issues & Solutions

### Issue: Python version too old
**Solution**: Install Python 3.10+ from python.org or use pyenv

### Issue: AWS CLI not configured
**Solution**: Run `aws configure` and enter your credentials

### Issue: Virtual environment not activating
**Solution**: 
- On macOS/Linux: `source venv/bin/activate`
- On Windows: `venv\Scripts\activate`

### Issue: Package installation fails
**Solution**: 
- Upgrade pip: `pip install --upgrade pip`
- Install packages one by one to identify problematic ones
- On macOS M1/M2: Some packages may need Rosetta or special builds

### Issue: OpenAI API key not working
**Solution**: 
- Verify key is correct (starts with 'sk-')
- Check account has credits
- Test with: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`

## Next Steps

Once checklist is complete:
1. Run initial EDA on job postings dataset
2. Start prompt engineering experiments
3. Build basic resume parser prototype
4. Test LLM integration with sample data

## Time Budget

- Setup and configuration: 2-3 hours
- Data collection: 1 hour
- Initial testing and verification: 1 hour
- **Total Day 1 Morning**: ~4 hours
