"""Unit tests for SQLAlchemy models."""
from app.models.user import User, Skill
from app.models.job import Job
from app.models.application import Application

def test_create_user_and_skill(db_session):
    """Test user creation and serialization."""
    user = User(
        name="Jordan Lee",
        email="jordan@example.com",
        current_role="Software Engineer",
        years_experience=4.0,
        target_roles=["Backend Lead"],
        preferred_locations=["Remote"],
        preferred_work_mode="remote"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.name == "Jordan Lee"

    skill = Skill(
        user_id=user.id,
        name="Python",
        proficiency="expert",
        years_experience=4.0,
        verified=1
    )
    db_session.add(skill)
    db_session.commit()

    skill_dict = skill.to_dict()
    assert skill_dict["name"] == "Python"
    assert skill_dict["verified"] is True

def test_create_job(db_session):
    """Test job listing model storage."""
    job = Job(
        title="Backend Engineer",
        company="Scale Corp",
        description="We need a strong Python FastAPI developer.",
        required_skills=["Python", "FastAPI", "SQL"],
        technologies=["FastAPI", "PostgreSQL"]
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    assert job.id is not None
    assert "FastAPI" in job.required_skills
