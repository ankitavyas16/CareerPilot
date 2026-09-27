"""User and profile schemas."""
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class SkillSchema(BaseModel):
    name: str
    proficiency: str  # beginner, intermediate, advanced, expert
    years_experience: float = 0
    verified: bool = False

class ExperienceSchema(BaseModel):
    company: str
    title: str
    description: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    location: Optional[str] = None
    responsibilities: List[str] = []
    achievements: List[str] = []

class EducationSchema(BaseModel):
    school: str
    degree: str
    field: str
    graduation_date: Optional[str] = None
    description: Optional[str] = None

class ProjectSchema(BaseModel):
    name: str
    description: str
    url: Optional[str] = None
    technologies: List[str] = []
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class ResumeSchema(BaseModel):
    name: str
    content: str
    keywords: List[str] = []

class UserCreateSchema(BaseModel):
    name: str
    email: str
    current_role: Optional[str] = None
    years_experience: float = 0
    target_roles: List[str] = []
    preferred_locations: List[str] = []
    preferred_work_mode: str = "hybrid"
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = "USD"
    learning_goals: List[str] = []

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    current_role: Optional[str] = None
    years_experience: Optional[float] = None
    target_roles: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    preferred_work_mode: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    learning_goals: Optional[List[str]] = None

class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: str
    current_role: Optional[str] = None
    years_experience: float = 0
    target_roles: List[str] = []
    preferred_locations: List[str] = []
    preferred_work_mode: str = "hybrid"
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    learning_goals: List[str] = []

from pydantic import BaseModel, ConfigDict

# inside UserResponseSchema, JobResponseSchema, ApplicationResponseSchema:
model_config = ConfigDict(from_attributes=True)

