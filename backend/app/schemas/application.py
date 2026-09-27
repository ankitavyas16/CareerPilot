"""Application schemas."""
from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel

class ApplicationCreateSchema(BaseModel):
    job_id: Optional[int] = None
    company: str
    role: str
    job_url: Optional[str] = None
    recruiter_name: Optional[str] = None
    recruiter_email: Optional[str] = None
    notes: Optional[str] = None

class ApplicationUpdateSchema(BaseModel):
    status: Optional[str] = None
    interview_date: Optional[datetime] = None
    interview_type: Optional[str] = None
    interview_notes: Optional[str] = None
    recruiter_name: Optional[str] = None
    recruiter_email: Optional[str] = None
    notes: Optional[str] = None
    next_followup_date: Optional[datetime] = None

class ApplicationResponseSchema(BaseModel):
    id: int
    company: str
    role: str
    status: str
    date_applied: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    recruiter_name: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

from pydantic import BaseModel, ConfigDict

# inside UserResponseSchema, JobResponseSchema, ApplicationResponseSchema:
model_config = ConfigDict(from_attributes=True)

