"""AI Analysis & Career Agent Routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User, Skill
from app.models.job import Job
from app.models.application import Application
from app.schemas.job import JobAnalysisRequestSchema
from app.tools.llm_service import LLMService

router = APIRouter(prefix="/analysis", tags=["AI Agent Analysis"])
llm_service = LLMService()

@router.post("/analyze-jd")
def analyze_job_description(payload: JobAnalysisRequestSchema):
    """Parse and extract structured skills, responsibilities, and metadata from raw JD text."""
    if not payload.jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty.")
    
    result = llm_service.analyze_jd(payload.jd_text)
    return result

@router.get("/match-job/{job_id}")
def match_job_with_candidate(job_id: int, db: Session = Depends(get_db)):
    """Evaluate candidate profile against a specific job posting."""
    user = db.query(User).first()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User profile not found. Please create one.")
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    skills = [s.name for s in db.query(Skill).filter(Skill.user_id == user.id).all()]
    candidate_skills_lower = {s.lower() for s in skills}
    job_required_skills = job.required_skills or []

    matching = [s for s in job_required_skills if s.lower() in candidate_skills_lower]
    missing = [s for s in job_required_skills if s.lower() not in candidate_skills_lower]

    match_score = len(matching) / len(job_required_skills) if job_required_skills else 0.8
    match_score = round(min(1.0, match_score), 2)

    recommendation = "apply" if match_score >= 0.7 else ("learn_and_apply" if match_score >= 0.4 else "skip")

    return {
        "job_id": job.id,
        "title": job.title,
        "company": job.company,
        "match_score": match_score,
        "match_percentage": int(match_score * 100),
        "matching_skills": matching,
        "missing_skills": missing,
        "experience_match": user.years_experience >= 2.0,
        "location_match": True,
        "work_mode_match": job.work_mode in ["remote", user.preferred_work_mode],
        "recommendation": recommendation,
        "reason": f"Matched {len(matching)} of {len(job_required_skills)} required skills.",
    }

@router.get("/daily-briefing")
def get_daily_briefing(db: Session = Depends(get_db)):
    """Generate daily briefing dashboard metrics."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found.")

    jobs = db.query(Job).all()
    user_skills = {s.name.lower() for s in db.query(Skill).filter(Skill.user_id == user.id).all()}

    top_missing_skills = {}
    for j in jobs:
        for req in (j.required_skills or []):
            if req.lower() not in user_skills:
                top_missing_skills[req] = top_missing_skills.get(req, 0) + 1

    top_5_missing = sorted(top_missing_skills.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Get applications needing follow-up
    applications = db.query(Application).filter(Application.user_id == user.id).all()
    pending_followups = [a for a in applications if a.next_followup_date]

    return {
        "greeting": f"Good morning, {user.name}!",
        "target_roles": user.target_roles,
        "total_jobs_tracked": len(jobs),
        "applications_count": len(applications),
        "pending_interviews": len([a for a in applications if a.status == "interview"]),
        "in_demand_missing_skills": [{"skill": s[0], "frequency": s[1]} for s in top_5_missing],
        "today_learning_focus": user.learning_goals[0] if user.learning_goals else "Review core skills",
        "recommended_action": "Review upcoming interviews and prepare with practice questions.",
    }

@router.post("/match-jobs")
def batch_match_jobs(db: Session = Depends(get_db)):
    """Match all available jobs against candidate profile and return ranked list."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found.")

    jobs = db.query(Job).all()
    skills = {s.name.lower(): s.proficiency for s in db.query(Skill).filter(Skill.user_id == user.id).all()}

    matches = []
    for job in jobs:
        job_required = set(s.lower() for s in (job.required_skills or []))
        user_has = set(skills.keys())
        matched_skills = list(job_required & user_has)
        missing_skills = list(job_required - user_has)

        match_score = len(matched_skills) / len(job_required) if job_required else 0.5
        match_score = round(min(1.0, match_score), 2)

        matches.append({
            "job_id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "work_mode": job.work_mode,
            "match_score": match_score,
            "match_percentage": int(match_score * 100),
            "matching_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendation": "apply" if match_score >= 0.7 else ("review" if match_score >= 0.4 else "skip"),
        })

    # Sort by match score descending
    matches = sorted(matches, key=lambda x: x["match_score"], reverse=True)
    return {"total_matches": len(matches), "ranked_jobs": matches}
