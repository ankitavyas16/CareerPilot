"""Interview feedback and evaluation models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float
from app.db.database import Base

class InterviewFeedback(Base):
    """Interview results and feedback."""

    __tablename__ = "interview_feedback"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)

    interview_date = Column(DateTime, default=datetime.utcnow)
    interview_type = Column(String)  # technical, behavioral, screening

    interviewer_name = Column(String, nullable=True)
    overall_feedback = Column(Text, nullable=True)
    performance_score = Column(Float, nullable=True)  # 1-10

    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    questions_asked = Column(JSON, default=list)

    outcome = Column(String, nullable=True)  # advance, reject, pending
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "interview_date": self.interview_date.isoformat() if self.interview_date else None,
            "interview_type": self.interview_type,
            "overall_feedback": self.overall_feedback,
            "performance_score": self.performance_score,
            "strengths": self.strengths or [],
            "weaknesses": self.weaknesses or [],
            "outcome": self.outcome,
        }
