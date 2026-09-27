"""Application tracking routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.application import Application
from app.schemas.application import ApplicationCreateSchema, ApplicationUpdateSchema

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.get("")
@router.get("/")
def list_applications(db: Session = Depends(get_db)):
    """List all tracked job applications."""
    apps = db.query(Application).order_by(Application.created_at.desc()).all()
    return [a.to_dict() for a in apps]

@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_application(payload: ApplicationCreateSchema, db: Session = Depends(get_db)):
    """Track a new job application."""
    app_entry = Application(
        user_id=1,
        job_id=payload.job_id,
        company=payload.company,
        role=payload.role,
        job_url=payload.job_url,
        recruiter_name=payload.recruiter_name,
        recruiter_email=payload.recruiter_email,
        notes=payload.notes,
        status="applied",
    )
    db.add(app_entry)
    db.commit()
    db.refresh(app_entry)
    return app_entry.to_dict()
