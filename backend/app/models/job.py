"""Job models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from app.db.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    description = Column(Text)
    url = Column(String, nullable=True)
    experience_required = Column(String, nullable=True)
    location = Column(String, nullable=True)
    work_mode = Column(String, nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String, default="USD")
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    technologies = Column(JSON, default=list)
    key_responsibilities = Column(JSON, default=list)
    keywords = Column(JSON, default=list)
    source = Column(String, default="manual")
    source_id = Column(String, nullable=True)
    posted_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "work_mode": self.work_mode,
            "url": self.url,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "required_skills": self.required_skills or [],
            "preferred_skills": self.preferred_skills or [],
            "technologies": self.technologies or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

class JobAnalysis(Base):
    __tablename__ = "job_analysis"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    summary = Column(Text)
    matching_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    interview_topics = Column(JSON, default=list)
    ats_keywords = Column(JSON, default=list)
    difficulty_score = Column(Float, default=0.5)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "summary": self.summary,
            "matching_skills": self.matching_skills or [],
            "missing_skills": self.missing_skills or [],
            "interview_topics": self.interview_topics or [],
            "ats_keywords": self.ats_keywords or [],
            "difficulty_score": self.difficulty_score,
        }
