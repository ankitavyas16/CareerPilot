"""Application and interview models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from app.db.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    job_id = Column(Integer, index=True)
    company = Column(String, index=True)
    role = Column(String, index=True)
    job_url = Column(String, nullable=True)
    status = Column(String, index=True, default="saved")
    date_found = Column(DateTime, default=datetime.utcnow)
    date_applied = Column(DateTime, nullable=True)
    date_last_contact = Column(DateTime, nullable=True)
    next_followup_date = Column(DateTime, nullable=True)
    interview_date = Column(DateTime, nullable=True)
    interview_type = Column(String, nullable=True)
    interview_notes = Column(Text, nullable=True)
    interview_prepared = Column(Integer, default=0)
    recruiter_name = Column(String, nullable=True)
    recruiter_email = Column(String, nullable=True)
    recruiter_phone = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    resume_used = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "job_url": self.job_url,
            "status": self.status,
            "date_applied": self.date_applied.isoformat() if self.date_applied else None,
            "interview_date": self.interview_date.isoformat() if self.interview_date else None,
            "recruiter_name": self.recruiter_name,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class InterviewPrep(Base):
    __tablename__ = "interview_prep"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    technical_questions = Column(JSON, default=list)
    behavioral_questions = Column(JSON, default=list)
    jd_specific_questions = Column(JSON, default=list)
    preparation_notes = Column(Text, nullable=True)
    company_research = Column(Text, nullable=True)
    story_bank = Column(JSON, default=list)
    practice_count = Column(Integer, default=0)
    last_practice = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "technical_questions": self.technical_questions or [],
            "behavioral_questions": self.behavioral_questions or [],
            "jd_specific_questions": self.jd_specific_questions or [],
            "preparation_notes": self.preparation_notes,
            "practice_count": self.practice_count,
        }
