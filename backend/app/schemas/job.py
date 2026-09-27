"""Job schemas."""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class JobCreateSchema(BaseModel):
    title: str
    company: str
    description: str
    url: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = "hybrid"
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: Optional[str] = "USD"

class JobAnalysisRequestSchema(BaseModel):
    jd_text: str
    job_id: Optional[int] = None

class JobAnalysisResponseSchema(BaseModel):
    summary: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    technologies: List[str] = []
    key_responsibilities: List[str] = []
    keywords: List[str] = []
    estimated_experience: str = "Not specified"

class JobResponseSchema(BaseModel):
    id: int
    title: str
    company: str
    location: Optional[str] = None
    work_mode: Optional[str] = None
    url: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    technologies: List[str] = []
    created_at: Optional[datetime] = None

from pydantic import BaseModel, ConfigDict

# inside UserResponseSchema, JobResponseSchema, ApplicationResponseSchema:
model_config = ConfigDict(from_attributes=True)

