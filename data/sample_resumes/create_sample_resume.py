"""
Create a sample PDF resume for testing the Resume Coach application.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def create_sample_resume():
    """Create a sample software engineer resume PDF."""
    
    filename = "john_doe_resume.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1f77b4',
        spaceAfter=12,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2ca02c',
        spaceAfter=6,
        spaceBefore=12,
    )
    
    # Header
    story.append(Paragraph("JOHN DOE", title_style))
    story.append(Paragraph("Software Engineer", styles['Normal']))
    story.append(Paragraph("Email: john.doe@email.com | Phone: (555) 123-4567", styles['Normal']))
    story.append(Paragraph("LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe", styles['Normal']))
    story.append(Paragraph("Location: San Francisco, CA", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    summary = """
    Software Engineer with 5 years of experience in full-stack web development. 
    Proficient in Python, JavaScript, and React. Strong background in building scalable 
    applications and RESTful APIs. Experienced in cloud technologies including AWS and Docker.
    """
    story.append(Paragraph(summary, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", heading_style))
    skills = """
    <b>Programming Languages:</b> Python, JavaScript, TypeScript, SQL<br/>
    <b>Frameworks:</b> React, Node.js, FastAPI, Django, Flask<br/>
    <b>Tools &amp; Technologies:</b> Git, Docker, AWS (EC2, S3, Lambda), PostgreSQL, MongoDB<br/>
    <b>Other:</b> REST APIs, CI/CD, Agile/Scrum, Test-Driven Development
    """
    story.append(Paragraph(skills, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Work Experience
    story.append(Paragraph("WORK EXPERIENCE", heading_style))
    
    # Job 1
    story.append(Paragraph("<b>Senior Software Engineer</b> - Tech Corp Inc.", styles['Normal']))
    story.append(Paragraph("<i>January 2021 - Present</i>", styles['Normal']))
    exp1 = """
    • Developed and maintained microservices architecture using Python and FastAPI<br/>
    • Built responsive web applications using React and TypeScript<br/>
    • Implemented CI/CD pipelines reducing deployment time by 40%<br/>
    • Collaborated with cross-functional teams in Agile environment<br/>
    • Mentored junior developers and conducted code reviews
    """
    story.append(Paragraph(exp1, styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    # Job 2
    story.append(Paragraph("<b>Software Engineer</b> - StartUp Solutions", styles['Normal']))
    story.append(Paragraph("<i>June 2019 - December 2020</i>", styles['Normal']))
    exp2 = """
    • Designed and implemented RESTful APIs serving 100K+ daily requests<br/>
    • Optimized database queries improving performance by 60%<br/>
    • Integrated third-party services including Stripe and Twilio<br/>
    • Wrote unit and integration tests achieving 85% code coverage
    """
    story.append(Paragraph(exp2, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    story.append(Paragraph("<b>Bachelor of Science in Computer Science</b>", styles['Normal']))
    story.append(Paragraph("University of California, Berkeley - Graduated: May 2019", styles['Normal']))
    story.append(Paragraph("GPA: 3.7/4.0", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Projects
    story.append(Paragraph("PROJECTS", heading_style))
    projects = """
    <b>E-Commerce Platform</b> - Built a full-stack e-commerce application using React and Django<br/>
    <b>Task Management App</b> - Developed a real-time collaboration tool with WebSocket support<br/>
    <b>Open Source Contributions</b> - Active contributor to FastAPI and React libraries
    """
    story.append(Paragraph(projects, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"Created sample resume: {filename}")
    return filename

if __name__ == "__main__":
    create_sample_resume()
