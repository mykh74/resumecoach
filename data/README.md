# Resume Coach - Data Directory

This directory contains datasets used for the Resume Coach application.

## Structure

```
data/
├── sample_resumes/     # Sample resumes for testing (PDF format)
├── job_postings/       # Job description datasets
└── README.md          # This file
```

## Data Sources

### Job Postings

Recommended Kaggle datasets:
- [LinkedIn Job Postings](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)
- [Indeed Job Postings](https://www.kaggle.com/datasets)
- [Data Science Job Postings](https://www.kaggle.com/datasets)

Download and place CSV/JSON files in `job_postings/` directory.

### Sample Resumes

- Collect 5-10 anonymized resumes in PDF format
- Place in `sample_resumes/` directory
- Use for testing and validation
- **IMPORTANT**: Never commit resumes with real personal information

## Data Format

### Job Postings Expected Format
```json
{
  "title": "Software Engineer",
  "company": "Tech Corp",
  "description": "Full job description text...",
  "requirements": "List of requirements...",
  "location": "San Francisco, CA",
  "posted_date": "2026-01-01"
}
```

### Resume Format
- PDF files only (for MVP)
- Standard resume structure with sections:
  - Contact Information
  - Summary/Objective
  - Experience
  - Education
  - Skills

## Privacy & Security

⚠️ **IMPORTANT**: 
- Do NOT commit real personal information
- Anonymize all resumes before adding to repository
- Use `.gitignore` to exclude sensitive data files
- Follow data protection regulations (GDPR, CCPA)

## Data Preparation

See notebooks for data preprocessing:
- `notebooks/eda.ipynb` - Exploratory data analysis
- `notebooks/data_preprocessing.ipynb` - Data cleaning and preparation
