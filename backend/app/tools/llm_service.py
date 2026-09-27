"""LLM service for AI agent interactions and resume parsing."""
import json
import logging
import re
from typing import Optional, Dict, Any, List
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

        # Only initialize OpenAI if key is set and not a placeholder
        if (
            self.provider == "openai"
            and self.api_key
            and not self.api_key.startswith("sk-your-")
            and len(self.api_key.strip()) > 10
        ):
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI client: {e}")
                self.client = None
        else:
            logger.info("No valid OpenAI API key provided; using local fallback parsing")

    def extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """Extract JSON from LLM response, handling markdown code blocks."""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pattern = r"```(?:json)?\s*(.*?)\s*```"
            matches = re.findall(pattern, response, re.DOTALL)
            if matches:
                try:
                    return json.loads(matches[0])
                except json.JSONDecodeError:
                    pass

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass

            logger.warning(f"Could not extract valid JSON from response: {response[:200]}")
            return {}

    def parse_resume_to_profile(self, resume_text: str) -> Dict[str, Any]:
        """Extract structured candidate details from resume text."""
        if not self.client:
            return self._fallback_resume_parse(resume_text)

        prompt = f"""Extract all structured candidate details from this resume text.

Resume Text:
{resume_text}

Return a valid JSON object matching this schema exactly:
{{
    "name": "Full Name",
    "email": "Email address or ''",
    "current_role": "Most recent title or target title",
    "years_experience": 3.0,
    "target_roles": ["Role 1", "Role 2"],
    "preferred_work_mode": "hybrid",
    "bio": "2-3 sentence executive summary",
    "skills": [
        {{"name": "Python", "proficiency": "advanced", "years_experience": 3.0}},
        {{"name": "SQL", "proficiency": "intermediate", "years_experience": 2.0}}
    ],
    "experience": [
        {{
            "company": "Company Name",
            "title": "Job Title",
            "start_date": "YYYY-MM",
            "end_date": "YYYY-MM or null if present",
            "location": "City, State or Remote",
            "description": "Short overview",
            "responsibilities": ["bullet point 1", "bullet point 2"],
            "achievements": ["achievement 1"]
        }}
    ],
    "education": [
        {{
            "school": "University Name",
            "degree": "B.S. / M.S. / etc.",
            "field": "Field of Study",
            "graduation_date": "YYYY-MM or YYYY"
        }}
    ],
    "projects": [
        {{
            "name": "Project Name",
            "description": "Short description",
            "technologies": ["tech1", "tech2"]
        }}
    ]
}}

Only extract factual data present in the text. Return JSON only."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=2500,
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content
            parsed = self.extract_json_from_response(content)
            return parsed if parsed else self._fallback_resume_parse(resume_text)
        except Exception as e:
            logger.error(f"Error parsing resume with LLM: {e}")
            return self._fallback_resume_parse(resume_text)

    def _fallback_resume_parse(self, text: str) -> Dict[str, Any]:
        """Heuristic section-based extraction when LLM is unavailable."""
        # Extract Email
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        email = email_match.group(0) if email_match else "candidate@example.com"

        # Extract Name from top lines
        non_empty_lines = [line.strip() for line in text.splitlines() if line.strip()]
        name = non_empty_lines[0] if non_empty_lines else "Candidate Name"
        if "@" in name or "http" in name.lower():
            name = "Candidate"

        # Detect Common Skills
        skill_catalog = [
            "python", "sql", "fastapi", "django", "flask", "docker", "kubernetes",
            "aws", "gcp", "azure", "machine learning", "deep learning", "pytorch",
            "tensorflow", "scikit-learn", "pandas", "numpy", "react", "javascript",
            "typescript", "git", "linux", "postgresql", "mysql", "tableau", "power bi"
        ]
        text_lower = text.lower()
        detected_skills = [
            {"name": s.title(), "proficiency": "intermediate", "years_experience": 2.0}
            for s in skill_catalog if re.search(r"\b" + re.escape(s) + r"\b", text_lower)
        ]

        # Extract Education
        education = []
        edu_keywords = ["university", "college", "institute", "bachelor", "master", "phd", "b.s.", "m.s.", "b.tech"]
        for line in non_empty_lines:
            if any(k in line.lower() for k in edu_keywords) and len(line) < 120:
                education.append({
                    "school": line,
                    "degree": "Degree / Study",
                    "field": "Computer Science / Relevant Field",
                    "graduation_date": "Completed"
                })
        if not education:
            education.append({
                "school": "University / College",
                "degree": "Degree",
                "field": "Relevant Field",
                "graduation_date": "Completed"
            })

        # Extract Experience
        experience = []
        job_title_keywords = ["engineer", "developer", "analyst", "intern", "manager", "lead", "specialist"]
        for line in non_empty_lines:
            if any(k in line.lower() for k in job_title_keywords) and len(line) < 70 and not line.endswith("."):
                experience.append({
                    "company": "Professional Experience",
                    "title": line,
                    "start_date": "2022-01",
                    "end_date": None,
                    "location": "Remote / Onsite",
                    "description": line,
                    "responsibilities": ["Executed core role responsibilities and project deliverables."],
                    "achievements": []
                })
        if not experience:
            experience.append({
                "company": "Company",
                "title": "Software / Data Professional",
                "start_date": "2022-01",
                "end_date": None,
                "location": "Onsite / Remote",
                "description": "Experience extracted from uploaded resume.",
                "responsibilities": ["Primary technical deliverables and team contributions."],
                "achievements": []
            })

        years_exp = max(1.0, round(len(detected_skills) * 0.4, 1))

        return {
            "name": name,
            "email": email,
            "current_role": experience[0]["title"] if experience else "Software Engineer",
            "years_experience": years_exp,
            "target_roles": ["Software Engineer", "Data Scientist", "AI Engineer"],
            "preferred_work_mode": "hybrid",
            "bio": f"Experienced professional with background in {', '.join([s['name'] for s in detected_skills[:4]]) if detected_skills else 'software development'}.",
            "skills": detected_skills,
            "experience": experience[:3],
            "education": education[:2],
            "projects": [
                {
                    "name": "Featured Project",
                    "description": "Key technical projects extracted from resume profile.",
                    "technologies": [s["name"] for s in detected_skills[:3]]
                }
            ],
        }

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
