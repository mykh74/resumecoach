"""
LLM Service - Orchestrates calls to language models for coaching analysis.
Supports multiple LLM providers (OpenAI, Anthropic, SageMaker).
"""

import os
import time
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from backend.prompts.templates import PromptTemplates
from backend.models.schema import Resume, JobDescription, CoachingReport, GapAnalysis, StrengthAnalysis

# Load environment variables
load_dotenv()


class LLMService:
    """Service for interacting with language models."""
    
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        Initialize LLM service.
        
        Args:
            provider: LLM provider ("openai", "anthropic", "sagemaker")
            model_name: Specific model to use
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
        """
        self.provider = provider
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize the LLM based on provider
        if provider == "openai":
            self.model_name = model_name or os.getenv("MODEL_NAME", "gpt-3.5-turbo")
            self.llm = ChatOpenAI(
                model=self.model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "anthropic":
            # Can add Anthropic support later
            raise NotImplementedError("Anthropic provider not yet implemented")
        elif provider == "sagemaker":
            # Can add SageMaker support later
            raise NotImplementedError("SageMaker provider not yet implemented")
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        self.prompt_templates = PromptTemplates()
    
    def generate_coaching_report(
        self,
        resume: Resume,
        job_description: JobDescription,
        session_id: str
    ) -> CoachingReport:
        """
        Generate a complete coaching report.
        
        Args:
            resume: Parsed resume data
            job_description: Parsed job description
            session_id: Unique session identifier
            
        Returns:
            Complete coaching report
        """
        start_time = time.time()
        
        # Convert to dicts for templating
        resume_dict = resume.model_dump()
        job_dict = job_description.model_dump()
        
        # Generate the coaching report using a comprehensive prompt
        full_report = self._generate_full_report(resume_dict, job_dict)
        
        # Parse the report to extract structured data
        coaching_report = self._parse_report_response(
            full_report,
            session_id,
            resume_dict,
            job_dict
        )
        
        processing_time = time.time() - start_time
        coaching_report.processing_time = processing_time
        coaching_report.model_used = self.model_name
        
        return coaching_report
    
    def generate_coaching_report_multi_step(
        self,
        resume: Resume,
        job_description: JobDescription,
        session_id: str
    ) -> CoachingReport:
        """
        Generate coaching report using multi-step approach.
        This provides more structured and thorough analysis.
        
        Args:
            resume: Parsed resume data
            job_description: Parsed job description
            session_id: Unique session identifier
            
        Returns:
            Complete coaching report
        """
        start_time = time.time()
        
        resume_dict = resume.model_dump()
        job_dict = job_description.model_dump()
        
        # Step 1: Fit Assessment
        fit_response = self._generate_fit_assessment(resume_dict, job_dict)
        fit_score, overall_assessment = self._parse_fit_assessment(fit_response)
        
        # Step 2: Gap Analysis
        gap_response = self._generate_gap_analysis(resume_dict, job_dict)
        gap_analysis = self._parse_gap_analysis(gap_response)
        
        # Step 3: Strength Analysis
        strength_response = self._generate_strength_analysis(resume_dict, job_dict)
        strength_analysis = self._parse_strength_analysis(strength_response)
        
        # Step 4: Resume Optimization
        optimization_response = self._generate_resume_optimization(resume_dict, job_dict)
        resume_improvements = self._parse_resume_improvements(optimization_response)
        
        # Step 5: Interview Prep
        interview_response = self._generate_interview_prep(resume_dict, job_dict)
        interview_tips, action_items = self._parse_interview_prep(interview_response)
        
        # Compile the report
        coaching_report = CoachingReport(
            session_id=session_id,
            fit_score=fit_score,
            overall_assessment=overall_assessment,
            gap_analysis=gap_analysis,
            strength_analysis=strength_analysis,
            resume_improvements=resume_improvements,
            interview_tips=interview_tips,
            action_items=action_items,
            general_advice=[
                "Tailor your resume specifically for this role",
                "Practice answering questions about any experience gaps",
                "Research the company culture and values",
                "Prepare specific examples using the STAR method"
            ],
            resume_summary=PromptTemplates._format_resume_summary(resume_dict),
            job_summary=PromptTemplates._format_job_summary(job_dict),
            model_used=self.model_name,
            processing_time=time.time() - start_time
        )
        
        return coaching_report
    
    def chat_response(
        self,
        question: str,
        context: Dict[str, Any],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a chat response based on context.
        
        Args:
            question: User's question
            context: Context including resume, job, and report
            conversation_history: Previous messages (optional)
            
        Returns:
            Response text
        """
        # Format the chat prompt
        prompt = PromptTemplates.format_chat_prompt(question, context)
        
        # Build messages
        messages = [
            SystemMessage(content=PromptTemplates.CHAT_SYSTEM_PROMPT.format(
                context_summary=str(context.get('summary', ''))[:500],
                report_summary=str(context.get('report_summary', ''))[:500]
            ))
        ]
        
        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                if msg['role'] == 'user':
                    messages.append(HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    messages.append(SystemMessage(content=msg['content']))
        
        # Add current question
        messages.append(HumanMessage(content=prompt))
        
        # Generate response
        response = self.llm.invoke(messages)
        return response.content
    
    # Private helper methods
    
    def _generate_full_report(self, resume: Dict, job: Dict) -> str:
        """Generate full coaching report in one call."""
        system_message = SystemMessage(content=PromptTemplates.SYSTEM_COACH)
        human_message = HumanMessage(
            content=PromptTemplates.format_coaching_report_prompt(resume, job)
        )
        
        response = self.llm.invoke([system_message, human_message])
        return response.content
    
    def _generate_fit_assessment(self, resume: Dict, job: Dict) -> str:
        """Generate fit assessment."""
        prompt = PromptTemplates.format_fit_assessment(resume, job)
        system_message = SystemMessage(content=PromptTemplates.SYSTEM_ANALYZER)
        human_message = HumanMessage(content=prompt)
        
        response = self.llm.invoke([system_message, human_message])
        return response.content
    
    def _generate_gap_analysis(self, resume: Dict, job: Dict) -> str:
        """Generate gap analysis."""
        prompt = PromptTemplates.format_gap_analysis(resume, job)
        system_message = SystemMessage(content=PromptTemplates.SYSTEM_ANALYZER)
        human_message = HumanMessage(content=prompt)
        
        response = self.llm.invoke([system_message, human_message])
        return response.content
    
    def _generate_strength_analysis(self, resume: Dict, job: Dict) -> str:
        """Generate strength analysis."""
        prompt = PromptTemplates.format_strength_analysis(resume, job)
        system_message = SystemMessage(content=PromptTemplates.SYSTEM_ANALYZER)
        human_message = HumanMessage(content=prompt)
        
        response = self.llm.invoke([system_message, human_message])
        return response.content
    
    def _generate_resume_optimization(self, resume: Dict, job: Dict) -> str:
        """Generate resume optimization suggestions."""
        prompt = PromptTemplates.RESUME_OPTIMIZATION_PROMPT.format(
            resume_summary=PromptTemplates._format_resume_summary(resume),
            job_title=job.get('title', 'N/A'),
            company=job.get('company', 'N/A'),
            key_requirements=', '.join(job.get('required_skills', [])[:5])
        )
        system_message = SystemMessage(content=PromptTemplates.SYSTEM_COACH)
        human_message = HumanMessage(content=prompt)
        
        response = self.llm.invoke([system_message, human_message])
        return response.content
    
    def _generate_interview_prep(self, resume: Dict, job: Dict) -> str:
        """Generate interview preparation tips."""
        prompt = PromptTemplates.INTERVIEW_PREP_PROMPT.format(
            resume_summary=PromptTemplates._format_resume_summary(resume),
            job_title=job.get('title', 'N/A'),
            job_summary=PromptTemplates._format_job_summary(job),
            job_requirements=PromptTemplates._format_job_requirements(job)
        )
        system_message = SystemMessage(content=PromptTemplates.SYSTEM_COACH)
        human_message = HumanMessage(content=prompt)
        
        response = self.llm.invoke([system_message, human_message])
        return response.content
    
    # Response parsing methods
    
    def _parse_report_response(
        self,
        response: str,
        session_id: str,
        resume: Dict,
        job: Dict
    ) -> CoachingReport:
        """Parse the full report response into structured data."""
        # Extract fit score (look for patterns like "Score: 8/10" or "8 out of 10")
        import re
        fit_score = 7.0  # Default
        score_match = re.search(r'(?:score|rating)[:|\s]+(\d+(?:\.\d+)?)\s*(?:/|\s*out of)\s*10', response, re.IGNORECASE)
        if score_match:
            fit_score = float(score_match.group(1))
        
        # For simplicity, treat the full response as overall assessment
        # In production, would parse sections more carefully
        return CoachingReport(
            session_id=session_id,
            fit_score=fit_score,
            overall_assessment=response[:500],  # First part as summary
            gap_analysis=GapAnalysis(
                missing_skills=self._extract_list_from_text(response, "missing", "gap"),
                recommendations=["Review the detailed analysis below"]
            ),
            strength_analysis=StrengthAnalysis(
                highlights=self._extract_list_from_text(response, "strength", "match")
            ),
            resume_improvements=self._extract_list_from_text(response, "improve", "recommend"),
            interview_tips=self._extract_list_from_text(response, "interview", "question"),
            action_items=self._extract_list_from_text(response, "action", "next step"),
            general_advice=[response[-200:]],  # Last part as advice
            resume_summary=PromptTemplates._format_resume_summary(resume),
            job_summary=PromptTemplates._format_job_summary(job)
        )
    
    def _parse_fit_assessment(self, response: str) -> tuple[float, str]:
        """Parse fit assessment response."""
        import re
        
        # Extract score
        score = 7.0
        score_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:/|\s*out of)\s*10', response)
        if score_match:
            score = float(score_match.group(1))
        
        # Overall assessment is the response itself
        return score, response
    
    def _parse_gap_analysis(self, response: str) -> GapAnalysis:
        """Parse gap analysis response."""
        return GapAnalysis(
            missing_skills=self._extract_list_from_text(response, "missing", "lack"),
            missing_qualifications=self._extract_list_from_text(response, "qualification", "requirement"),
            experience_gap=response[:200] if "experience" in response.lower() else None,
            recommendations=self._extract_list_from_text(response, "address", "recommend")
        )
    
    def _parse_strength_analysis(self, response: str) -> StrengthAnalysis:
        """Parse strength analysis response."""
        return StrengthAnalysis(
            matching_skills=self._extract_list_from_text(response, "match", "has"),
            unique_strengths=self._extract_list_from_text(response, "unique", "advantage"),
            relevant_experiences=self._extract_list_from_text(response, "experience", "relevant"),
            highlights=self._extract_list_from_text(response, "highlight", "emphasize")
        )
    
    def _parse_resume_improvements(self, response: str) -> List[str]:
        """Parse resume improvement suggestions."""
        return self._extract_list_from_text(response, "improve", "add", "update")
    
    def _parse_interview_prep(self, response: str) -> tuple[List[str], List[str]]:
        """Parse interview prep response."""
        tips = self._extract_list_from_text(response, "tip", "prepare", "question")
        actions = self._extract_list_from_text(response, "action", "do", "step")
        return tips, actions
    
    def _extract_list_from_text(self, text: str, *keywords) -> List[str]:
        """Extract list items from text based on keywords."""
        import re
        
        items = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Check if line contains any keyword
            if any(kw.lower() in line.lower() for kw in keywords):
                # Clean up list markers
                cleaned = re.sub(r'^[\d\.\-\*\•\►\→]+\s*', '', line)
                if cleaned and len(cleaned) > 10:
                    items.append(cleaned[:200])  # Limit length
        
        return items[:15]  # Return max 15 items
