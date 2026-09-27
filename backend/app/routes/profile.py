"""User profile and career memory routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User, Skill, Experience, Education, Project
from app.schemas.user import UserCreateSchema, UserUpdateSchema

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("")
@router.get("/")
def get_user_profile(db: Session = Depends(get_db)):
    """Retrieve the primary candidate profile with all career memory."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found. Please create one.")

    skills = db.query(Skill).filter(Skill.user_id == user.id).all()
    experience = db.query(Experience).filter(Experience.user_id == user.id).all()
    education = db.query(Education).filter(Education.user_id == user.id).all()
    projects = db.query(Project).filter(Project.user_id == user.id).all()

    profile_data = user.to_dict()
    profile_data["skills"] = [s.to_dict() for s in skills]
    profile_data["experience"] = [e.to_dict() for e in experience]
    profile_data["education"] = [ed.to_dict() for ed in education]
    profile_data["projects"] = [p.to_dict() for p in projects]

    return profile_data

@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_or_update_profile(payload: UserCreateSchema, db: Session = Depends(get_db)):
    """Create or update user profile."""
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        user = User(
            name=payload.name,
            email=payload.email,
            current_role=payload.current_role,
            years_experience=payload.years_experience,
            target_roles=payload.target_roles,
            preferred_locations=payload.preferred_locations,
            preferred_work_mode=payload.preferred_work_mode,
            salary_min=payload.salary_min,
            salary_max=payload.salary_max,
            salary_currency=payload.salary_currency,
            learning_goals=payload.learning_goals,
        )
        db.add(user)
    else:
        user.name = payload.name
        user.current_role = payload.current_role
        user.years_experience = payload.years_experience
        user.target_roles = payload.target_roles
        user.preferred_locations = payload.preferred_locations
        user.preferred_work_mode = payload.preferred_work_mode
        user.salary_min = payload.salary_min
        user.salary_max = payload.salary_max
        user.learning_goals = payload.learning_goals

    db.commit()
    db.refresh(user)
    return user.to_dict()
