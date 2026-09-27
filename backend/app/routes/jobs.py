"""Job management and matching routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreateSchema

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("")
@router.get("/")
def list_jobs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List stored job descriptions."""
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return [j.to_dict() for j in jobs]

@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreateSchema, db: Session = Depends(get_db)):
    """Create a new job posting entry."""
    job = Job(
        title=payload.title,
        company=payload.company,
        description=payload.description,
        url=payload.url,
        location=payload.location,
        work_mode=payload.work_mode or "hybrid",
        required_skills=[],
        preferred_skills=[],
        technologies=[],
        key_responsibilities=[],
        keywords=[],
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job.to_dict()

@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get single job details."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.to_dict()
