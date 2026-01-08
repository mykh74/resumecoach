"""
Prompt Templates for Resume Coach.
Contains all prompt engineering strategies for generating coaching advice.
"""

from typing import Dict, Any


class PromptTemplates:
    """Collection of prompt templates for different coaching tasks."""
    
    # System prompts
    SYSTEM_COACH = """You are an expert career coach and resume consultant with over 15 years of experience. You specialize in helping candidates optimize their job applications and match their qualifications to job requirements.

Your advice is:
- Specific and actionable
- Honest and constructive
- Based on industry best practices
- Tailored to the individual's background
- Encouraging yet realistic

You understand various industries, job markets, and hiring practices."""

    SYSTEM_ANALYZER = """You are an expert at analyzing resumes and job descriptions. You can identify:
- Key skills and qualifications
- Experience levels and requirements
- Gaps between candidate qualifications and job needs
- Unique strengths and competitive advantages
- Areas for improvement

You provide structured, data-driven analysis."""

    # Main coaching report prompt
    COACHING_REPORT_PROMPT = """Analyze the following resume and job description, then provide comprehensive coaching advice.

**Resume Summary:**
{resume_summary}

**Job Description Summary:**
{job_summary}

**Detailed Resume:**
{resume_details}

**Detailed Job Requirements:**
{job_requirements}

Provide a detailed coaching report with the following sections:

1. **Overall Fit Assessment (Score 0-10)**
   - Give an honest score from 0-10 indicating how well the candidate matches the role
   - Provide a brief explanation of the score

2. **Gap Analysis**
   - List missing skills or qualifications
   - Identify any experience gaps
   - Note missing certifications or requirements

3. **Strengths to Highlight**
   - Identify matching skills and experiences
   - Point out unique competitive advantages
   - Highlight relevant achievements

4. **Resume Improvements**
   - Specific suggestions to better align resume with job
   - Keywords or phrases to emphasize
   - Sections that need strengthening

5. **Interview Preparation Tips**
   - Key talking points to prepare
   - Potential interview questions based on requirements
   - How to address any gaps in qualifications

6. **Action Items**
   - Concrete next steps to improve candidacy
   - Skills to develop or highlight
   - Networking or research recommendations

Be specific, actionable, and encouraging. Format your response clearly with section headers."""

    # Structured analysis prompts (for multi-step approach)
    
    FIT_ASSESSMENT_PROMPT = """You are a career coach evaluating how well a candidate fits a job role.

**Candidate Background:**
{resume_summary}

**Job Role:**
{job_summary}

Provide:
1. An overall fit score from 0-10 (where 0 = completely unqualified, 10 = perfect match)
2. A 2-3 sentence explanation of the score
3. The candidate's strongest 3 qualifications for this role
4. The top 3 concerns or gaps

Be honest and constructive."""

    GAP_ANALYSIS_PROMPT = """Analyze the gaps between this candidate's qualifications and the job requirements.

**Candidate's Skills and Experience:**
{resume_skills}

**Job Requirements:**
{job_requirements}

Identify:
1. **Missing Critical Skills**: Skills marked as required that the candidate lacks
2. **Experience Gaps**: Any experience level or domain mismatches
3. **Missing Qualifications**: Certifications, degrees, or credentials not present
4. **How to Address Each Gap**: For each gap, suggest if it's addressable and how

Be thorough but focus on the most important gaps first."""

    STRENGTH_ANALYSIS_PROMPT = """Identify the candidate's competitive strengths for this role.

**Candidate's Background:**
{resume_experiences}
{resume_skills}

**Job Requirements:**
{job_requirements}

Provide:
1. **Matching Skills**: Skills the candidate has that directly match requirements (be specific)
2. **Relevant Experiences**: Work experiences that align with job responsibilities
3. **Unique Advantages**: What makes this candidate stand out (e.g., unique combinations of skills, impressive achievements)
4. **Recommended Highlights**: What the candidate should emphasize in their application

Focus on concrete, provable strengths."""

    RESUME_OPTIMIZATION_PROMPT = """Suggest specific improvements to optimize this resume for the target job.

**Current Resume Highlights:**
{resume_summary}

**Target Job:**
{job_title} at {company}

**Key Job Requirements:**
{key_requirements}

Provide:
1. **Keywords to Add**: Specific terms from the job description to incorporate
2. **Experience Bullets to Emphasize**: Which experiences are most relevant
3. **Skills Section Updates**: How to reorder or enhance skills section
4. **Summary/Objective Rewrite**: Suggested opening statement tailored to this role
5. **Format/Structure Tips**: Any layout improvements

Be very specific with examples."""

    INTERVIEW_PREP_PROMPT = """Prepare interview guidance for this candidate applying to this role.

**Candidate Background:**
{resume_summary}

**Target Role:**
{job_title} - {job_summary}

**Key Requirements:**
{job_requirements}

Provide:
1. **Likely Interview Questions** (5-7 questions based on job requirements)
2. **How to Answer Gap Questions**: If there are experience gaps, how to address them
3. **STAR Method Examples**: Suggest 2-3 stories from their experience to prepare
4. **Questions to Ask**: 3-5 good questions for the candidate to ask interviewers
5. **Red Flags to Avoid**: Common mistakes to avoid based on the role

Be practical and specific to this role."""

    # Chat conversation prompts
    
    CHAT_SYSTEM_PROMPT = """You are a helpful career coach chatbot assisting a job seeker. You have access to their resume and the job description they're interested in.

Context:
{context_summary}

Previous Coaching Report Summary:
{report_summary}

Answer the user's questions based on this context. Be:
- Friendly and encouraging
- Specific and actionable
- Honest about challenges
- Supportive of their goals

If asked about something outside your context, acknowledge what you know and what you don't."""

    CHAT_FOLLOWUP_PROMPT = """Based on our coaching analysis and the user's question, provide a helpful response.

**User Question:** {user_question}

**Relevant Context:**
{relevant_context}

Provide a clear, actionable answer. If the question relates to gaps or concerns, be constructive and suggest concrete steps."""

    # Comparison and matching prompts
    
    SKILLS_MATCH_PROMPT = """Compare the candidate's skills with job requirements.

**Candidate Skills:**
{candidate_skills}

**Required Skills:**
{required_skills}

**Preferred Skills:**
{preferred_skills}

For each required and preferred skill:
1. Check if candidate has it (yes/no/partial)
2. Rate proficiency if evident (beginner/intermediate/advanced)
3. Note where it appears in their resume

Provide a structured table format."""

    EXPERIENCE_MATCH_PROMPT = """Evaluate if the candidate's experience level matches the job requirements.

**Candidate Experience:**
- Total years: {total_years}
- Relevant experience: {relevant_experience}
- Industry background: {industries}

**Job Requirements:**
- Required experience: {required_years}
- Industry preference: {job_industry}
- Seniority level: {seniority}

Assessment:
1. Does experience level match? (under/match/exceed)
2. Is industry experience relevant?
3. Are there transferable experiences from other domains?
4. Overall experience fit score (0-10)"""

    # Quick assessment prompts
    
    QUICK_FIT_CHECK = """Quick assessment: Does this candidate meet the basic requirements?

Resume: {resume_summary}
Job: {job_summary}

Answer:
- Qualified (Yes/Maybe/No)
- One sentence why
- Top recommendation"""

    # Helper methods
    
    @staticmethod
    def format_coaching_report_prompt(resume: Dict[str, Any], job: Dict[str, Any]) -> str:
        """Format the main coaching report prompt with actual data."""
        return PromptTemplates.COACHING_REPORT_PROMPT.format(
            resume_summary=PromptTemplates._format_resume_summary(resume),
            job_summary=PromptTemplates._format_job_summary(job),
            resume_details=PromptTemplates._format_resume_details(resume),
            job_requirements=PromptTemplates._format_job_requirements(job)
        )
    
    @staticmethod
    def format_fit_assessment(resume: Dict[str, Any], job: Dict[str, Any]) -> str:
        """Format fit assessment prompt."""
        return PromptTemplates.FIT_ASSESSMENT_PROMPT.format(
            resume_summary=PromptTemplates._format_resume_summary(resume),
            job_summary=PromptTemplates._format_job_summary(job)
        )
    
    @staticmethod
    def format_gap_analysis(resume: Dict[str, Any], job: Dict[str, Any]) -> str:
        """Format gap analysis prompt."""
        return PromptTemplates.GAP_ANALYSIS_PROMPT.format(
            resume_skills=PromptTemplates._format_skills(resume.get('skills', [])),
            job_requirements=PromptTemplates._format_job_requirements(job)
        )
    
    @staticmethod
    def format_strength_analysis(resume: Dict[str, Any], job: Dict[str, Any]) -> str:
        """Format strength analysis prompt."""
        return PromptTemplates.STRENGTH_ANALYSIS_PROMPT.format(
            resume_experiences=PromptTemplates._format_experiences(resume.get('experiences', [])),
            resume_skills=PromptTemplates._format_skills(resume.get('skills', [])),
            job_requirements=PromptTemplates._format_job_requirements(job)
        )
    
    @staticmethod
    def format_chat_prompt(question: str, context: Dict[str, Any]) -> str:
        """Format chat conversation prompt."""
        return PromptTemplates.CHAT_FOLLOWUP_PROMPT.format(
            user_question=question,
            relevant_context=str(context)[:1000]  # Limit context size
        )
    
    # Private formatting helpers
    
    @staticmethod
    def _format_resume_summary(resume: Dict[str, Any]) -> str:
        """Create a concise resume summary."""
        parts = []
        
        if contact := resume.get('contact_info', {}):
            if contact.get('name'):
                parts.append(f"Name: {contact['name']}")
        
        if summary := resume.get('summary'):
            parts.append(f"Summary: {summary[:200]}")
        
        if skills := resume.get('skills', []):
            parts.append(f"Key Skills: {', '.join(skills[:10])}")
        
        if experiences := resume.get('experiences', []):
            exp_count = len(experiences)
            parts.append(f"Work Experience: {exp_count} positions")
            if experiences:
                latest = experiences[0]
                if isinstance(latest, dict):
                    parts.append(f"Current/Latest: {latest.get('title', 'N/A')} at {latest.get('company', 'N/A')}")
        
        if education := resume.get('education', []):
            if education and isinstance(education[0], dict):
                parts.append(f"Education: {education[0].get('degree', 'N/A')}")
        
        return '\n'.join(parts)
    
    @staticmethod
    def _format_job_summary(job: Dict[str, Any]) -> str:
        """Create a concise job summary."""
        parts = []
        
        if title := job.get('title'):
            parts.append(f"Title: {title}")
        
        if company := job.get('company'):
            parts.append(f"Company: {company}")
        
        if location := job.get('location'):
            parts.append(f"Location: {location}")
        
        if exp_level := job.get('experience_level'):
            parts.append(f"Experience Level: {exp_level}")
        
        if summary := job.get('summary'):
            parts.append(f"Overview: {summary[:200]}")
        
        return '\n'.join(parts)
    
    @staticmethod
    def _format_resume_details(resume: Dict[str, Any]) -> str:
        """Format detailed resume information."""
        parts = []
        
        if skills := resume.get('skills', []):
            parts.append(f"Skills: {', '.join(skills)}")
        
        if experiences := resume.get('experiences', []):
            parts.append("\nWork Experience:")
            for exp in experiences[:5]:  # Limit to recent
                if isinstance(exp, dict):
                    parts.append(f"- {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
                    if responsibilities := exp.get('responsibilities', []):
                        for resp in responsibilities[:3]:
                            parts.append(f"  • {resp}")
        
        if education := resume.get('education', []):
            parts.append("\nEducation:")
            for edu in education:
                if isinstance(edu, dict):
                    parts.append(f"- {edu.get('degree', 'N/A')} from {edu.get('institution', 'N/A')}")
        
        return '\n'.join(parts)
    
    @staticmethod
    def _format_job_requirements(job: Dict[str, Any]) -> str:
        """Format job requirements."""
        parts = []
        
        if required_skills := job.get('required_skills', []):
            parts.append(f"Required Skills: {', '.join(required_skills)}")
        
        if preferred_skills := job.get('preferred_skills', []):
            parts.append(f"Preferred Skills: {', '.join(preferred_skills)}")
        
        if requirements := job.get('requirements', []):
            parts.append("\nKey Requirements:")
            for req in requirements[:10]:
                if isinstance(req, dict):
                    parts.append(f"- [{req.get('category', 'N/A')}] {req.get('requirement', 'N/A')}")
        
        if responsibilities := job.get('responsibilities', []):
            parts.append("\nKey Responsibilities:")
            for resp in responsibilities[:5]:
                parts.append(f"- {resp}")
        
        return '\n'.join(parts)
    
    @staticmethod
    def _format_skills(skills: list) -> str:
        """Format skills list."""
        if not skills:
            return "No skills listed"
        return ', '.join(skills[:20])
    
    @staticmethod
    def _format_experiences(experiences: list) -> str:
        """Format experiences list."""
        if not experiences:
            return "No experiences listed"
        
        parts = []
        for exp in experiences[:5]:
            if isinstance(exp, dict):
                parts.append(f"{exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
        
        return '\n'.join(parts)
