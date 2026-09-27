"""User and profile models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    current_role = Column(String, nullable=True)
    years_experience = Column(Float, default=0)
    target_roles = Column(JSON, default=list)
    preferred_locations = Column(JSON, default=list)
    preferred_work_mode = Column(String, default="hybrid")
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String, default="USD")
    learning_goals = Column(JSON, default=list)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "current_role": self.current_role,
            "years_experience": self.years_experience,
            "target_roles": self.target_roles or [],
            "preferred_locations": self.preferred_locations or [],
            "preferred_work_mode": self.preferred_work_mode,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "learning_goals": self.learning_goals or [],
            "bio": self.bio,
        }

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    name = Column(String, index=True)
    proficiency = Column(String)
    years_experience = Column(Float, default=0)
    verified = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "proficiency": self.proficiency,
            "years_experience": self.years_experience,
            "verified": bool(self.verified),
        }

class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    company = Column(String)
    title = Column(String)
    description = Column(Text, nullable=True)
    start_date = Column(String)
    end_date = Column(String, nullable=True)
    location = Column(String, nullable=True)
    responsibilities = Column(JSON, default=list)
    achievements = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "location": self.location,
            "responsibilities": self.responsibilities or [],
            "achievements": self.achievements or [],
        }

class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    school = Column(String)
    degree = Column(String)
    field = Column(String)
    graduation_date = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "school": self.school,
            "degree": self.degree,
            "field": self.field,
            "graduation_date": self.graduation_date,
            "description": self.description,
        }

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    name = Column(String)
    description = Column(Text)
    url = Column(String, nullable=True)
    technologies = Column(JSON, default=list)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "technologies": self.technologies or [],
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    name = Column(String)
    content = Column(Text)
    keywords = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "keywords": self.keywords or [],
        }
