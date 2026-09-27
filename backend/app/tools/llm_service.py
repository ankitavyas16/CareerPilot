"""LLM service for AI agent interactions."""
import json
import logging
import re
from typing import Optional, Dict, Any
from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

class LLMService:
    """Service for LLM API interactions with fallback graceful degradation."""

    def __init__(self):
        """Initialize LLM service."""
        self.provider = settings.llm_provider
        self.model = settings.openai_model
        self.api_key = settings.openai_api_key
        self.client = None

        if self.provider == "openai" and self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully")
            except ImportError:
                logger.warning("OpenAI library not installed; LLM features disabled")
        else:
            logger.info("LLM API key not configured; using fallback analysis")

    def extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """Extract JSON from LLM response, handling markdown code blocks."""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Look for JSON in markdown code blocks
            pattern = r"```(?:json)?\s*(.*?)\s*```"
            matches = re.findall(pattern, response, re.DOTALL)
            if matches:
                try:
                    return json.loads(matches[0])
                except json.JSONDecodeError:
                    pass

            # Try extracting { ... } pattern
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass

            logger.warning(f"Could not extract valid JSON from response: {response[:200]}")
            return {}

    def analyze_jd(self, jd_text: str) -> Dict[str, Any]:
        """Analyze job description and extract structured data."""
        if not self.client:
            return self._fallback_jd_analysis(jd_text)

        prompt = f"""Analyze this job description and extract structured information.

Job Description:
{jd_text}

Return a JSON object with:
{{
    "title": "Job title",
    "company": "Company name if mentioned",
    "location": "Location or 'Not specified'",
    "work_mode": "remote/hybrid/onsite or 'Not specified'",
    "experience_required": "e.g., '3-5 years' or 'Not specified'",
    "required_skills": ["skill1", "skill2"],
    "preferred_skills": ["skill1", "skill2"],
    "technologies": ["tech1", "tech2"],
    "key_responsibilities": ["resp1", "resp2"],
    "keywords": ["keyword1", "keyword2"],
    "summary": "2-3 sentence summary of the role"
}}

Be concise and accurate. Extract only what is explicitly mentioned."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content
            result = self.extract_json_from_response(content)
            return result if result else self._fallback_jd_analysis(jd_text)
        except Exception as e:
            logger.error(f"Error analyzing JD with LLM: {e}")
            return self._fallback_jd_analysis(jd_text)

    def _fallback_jd_analysis(self, jd_text: str) -> Dict[str, Any]:
        """Fallback analysis when LLM is unavailable."""
        skill_keywords = [
            "python", "sql", "java", "javascript", "r", "scala", "go", "rust",
            "machine learning", "deep learning", "nlp", "computer vision",
            "data analysis", "analytics", "tableau", "power bi", "looker",
            "aws", "gcp", "azure", "docker", "kubernetes",
            "react", "angular", "vue", "django", "flask", "fastapi",
            "spark", "hadoop", "airflow", "dbt",
        ]

        found_skills = [skill for skill in skill_keywords if skill in jd_text.lower()]

        # Extract location if mentioned
        location = "Not specified"
        if "remote" in jd_text.lower():
            location = "Remote"
        elif "san francisco" in jd_text.lower():
            location = "San Francisco, CA"
        elif "new york" in jd_text.lower():
            location = "New York, NY"

        return {
            "title": "Position Title",
            "company": "Company",
            "location": location,
            "work_mode": "remote" if "remote" in jd_text.lower() else "hybrid",
            "experience_required": "Not specified",
            "required_skills": found_skills[:5],
            "preferred_skills": found_skills[5:10],
            "technologies": found_skills,
            "key_responsibilities": [],
            "keywords": found_skills,
            "summary": "Job posting analysis (Full LLM analysis not available without API key)",
        }

    def compare_candidate_to_jd(
        self,
        candidate_skills: list,
        candidate_exp_years: float,
        jd_required_skills: list,
        jd_exp_required: str,
    ) -> Dict[str, Any]:
        """Compare candidate profile to job requirements."""
        candidate_skills_lower = {s.lower() for s in candidate_skills}
        jd_required_lower = {s.lower() for s in jd_required_skills}

        matching = list(candidate_skills_lower & jd_required_lower)
        missing = list(jd_required_lower - candidate_skills_lower)

        match_percentage = len(matching) / len(jd_required_lower) if jd_required_lower else 0.5
        match_percentage = round(min(1.0, match_percentage), 2)

        return {
            "matching_skills": matching,
            "missing_skills": missing,
            "match_percentage": match_percentage,
            "experience_match": candidate_exp_years >= 2.0,
            "recommendation": "apply" if match_percentage >= 0.7 else ("review" if match_percentage >= 0.4 else "skip"),
        }

    def generate_interview_questions(
        self,
        job_title: str,
        technologies: list,
        company: str,
    ) -> Dict[str, Any]:
        """Generate interview questions for a role."""
        if not self.client:
            return self._fallback_interview_questions(job_title, technologies)

        prompt = f"""Generate interview questions for a {job_title} role at {company}.

Technologies: {', '.join(technologies)}

Return a JSON object with:
{{
    "technical_questions": [
        {{"question": "q", "difficulty": "easy/medium/hard"}}
    ],
    "behavioral_questions": [
        {{"question": "q"}}
    ],
    "company_questions": [
        {{"question": "q"}}
    ]
}}

Generate 3-4 questions of each type."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content
            return self.extract_json_from_response(content)
        except Exception as e:
            logger.error(f"Error generating interview questions: {e}")
            return self._fallback_interview_questions(job_title, technologies)

    def _fallback_interview_questions(self, job_title: str, technologies: list) -> Dict[str, Any]:
        """Fallback interview questions when LLM unavailable."""
        return {
            "technical_questions": [
                {"question": f"Describe your experience with {technologies[0] if technologies else 'software development'}.", "difficulty": "medium"},
                {"question": "How do you approach debugging complex issues?", "difficulty": "medium"},
                {"question": "Walk us through a challenging project you completed.", "difficulty": "hard"},
            ],
            "behavioral_questions": [
                {"question": "Tell us about a time you worked in a team. How did you contribute?"},
                {"question": "Describe a situation where you had to learn something new quickly."},
                {"question": "How do you handle feedback and criticism?"},
            ],
            "company_questions": [
                {"question": f"Why are you interested in this {job_title} role?"},
                {"question": "What do you know about our company?"},
            ],
        }

    def generate_resume_suggestions(
        self,
        job_description: str,
        candidate_experience: list,
    ) -> Dict[str, Any]:
        """Generate resume suggestions for a job."""
        if not self.client:
            return {"suggestions": ["Align your experience with the job requirements.", "Emphasize relevant skills and projects."]}

        prompt = f"""Given this job description, suggest resume improvements:

Job Description:
{job_description}

Candidate Experience:
{', '.join(candidate_experience)}

Return a JSON object with:
{{
    "suggestions": ["suggestion1", "suggestion2"],
    "keywords_to_add": ["keyword1", "keyword2"]
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content
            return self.extract_json_from_response(content)
        except Exception as e:
            logger.error(f"Error generating resume suggestions: {e}")
            return {"suggestions": ["Review job requirements and tailor your resume accordingly."]}
