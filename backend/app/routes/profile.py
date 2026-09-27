"""User profile and career memory routes."""
import io
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from pypdf import PdfReader

from app.db.database import get_db
from app.models.user import User, Skill, Experience, Education, Project, Resume
from app.schemas.user import UserCreateSchema
from app.tools.llm_service import LLMService

router = APIRouter(prefix="/profile", tags=["Profile"])
llm_service = LLMService()

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
    resumes = db.query(Resume).filter(Resume.user_id == user.id).all()

    profile_data = user.to_dict()
    profile_data["skills"] = [s.to_dict() for s in skills]
    profile_data["experience"] = [e.to_dict() for e in experience]
    profile_data["education"] = [ed.to_dict() for ed in education]
    profile_data["projects"] = [p.to_dict() for p in projects]
    profile_data["resumes"] = [r.to_dict() for r in resumes]

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

@router.post("/parse-and-import")
async def parse_and_import_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload resume (PDF, TXT, MD), parse all sections via AI, 
    and auto-populate user profile, skills, experience, education, and projects.
    """
    filename = file.filename.lower() if file.filename else "resume.pdf"
    file_bytes = await file.read()
    raw_text = ""

    # 1. Extract text from uploaded document
    if filename.endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    raw_text += page_text + "\n"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read PDF: {str(e)}")
    elif filename.endswith((".txt", ".md")):
        raw_text = file_bytes.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a .pdf, .txt, or .md file."
        )

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Document contains no readable text.")

    # 2. Extract structured entities with AI
    parsed = llm_service.parse_resume_to_profile(raw_text)

    # 3. Upsert User Profile
    user = db.query(User).first()
    if not user:
        user = User(
            name=parsed.get("name") or "Candidate",
            email=parsed.get("email") or "candidate@example.com",
            current_role=parsed.get("current_role"),
            years_experience=float(parsed.get("years_experience") or 0.0),
            target_roles=parsed.get("target_roles") or [],
            preferred_work_mode=parsed.get("preferred_work_mode") or "hybrid",
            bio=parsed.get("bio") or "",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        if parsed.get("name"):
            user.name = parsed["name"]
        if parsed.get("email"):
            user.email = parsed["email"]
        if parsed.get("current_role"):
            user.current_role = parsed["current_role"]
        if parsed.get("years_experience"):
            user.years_experience = float(parsed["years_experience"])
        if parsed.get("target_roles"):
            user.target_roles = parsed["target_roles"]
        if parsed.get("bio"):
            user.bio = parsed["bio"]

    # 4. Save Raw Resume Version
    resume_record = Resume(
        user_id=user.id,
        name=file.filename or "Uploaded Resume",
        content=raw_text,
        keywords=[s["name"] for s in parsed.get("skills", []) if isinstance(s, dict) and "name" in s]
    )
    db.add(resume_record)

    # 5. Overwrite / Populate Skills
    db.query(Skill).filter(Skill.user_id == user.id).delete()
    for s in parsed.get("skills", []):
        if isinstance(s, dict) and s.get("name"):
            db.add(Skill(
                user_id=user.id,
                name=s["name"],
                proficiency=s.get("proficiency", "intermediate"),
                years_experience=float(s.get("years_experience", 1.0)),
                verified=1
            ))

    # 6. Overwrite / Populate Experience
    db.query(Experience).filter(Experience.user_id == user.id).delete()
    for exp in parsed.get("experience", []):
        if isinstance(exp, dict):
            db.add(Experience(
                user_id=user.id,
                company=exp.get("company", "Company"),
                title=exp.get("title", "Role"),
                start_date=exp.get("start_date", "2022-01"),
                end_date=exp.get("end_date"),
                location=exp.get("location"),
                description=exp.get("description"),
                responsibilities=exp.get("responsibilities", []),
                achievements=exp.get("achievements", [])
            ))

    # 7. Overwrite / Populate Education
    db.query(Education).filter(Education.user_id == user.id).delete()
    for edu in parsed.get("education", []):
        if isinstance(edu, dict):
            db.add(Education(
                user_id=user.id,
                school=edu.get("school", "University"),
                degree=edu.get("degree", "Degree"),
                field=edu.get("field", "Field"),
                graduation_date=edu.get("graduation_date")
            ))

    # 8. Overwrite / Populate Projects
    db.query(Project).filter(Project.user_id == user.id).delete()
    for proj in parsed.get("projects", []):
        if isinstance(proj, dict):
            db.add(Project(
                user_id=user.id,
                name=proj.get("name", "Project"),
                description=proj.get("description", ""),
                technologies=proj.get("technologies", [])
            ))

    db.commit()

    return {
        "status": "success",
        "message": "Resume parsed and profile updated across all sections successfully!",
        "parsed_summary": {
            "name": user.name,
            "email": user.email,
            "role": user.current_role,
            "skills_count": len(parsed.get("skills", [])),
            "experience_entries": len(parsed.get("experience", [])),
            "education_entries": len(parsed.get("education", [])),
            "projects_entries": len(parsed.get("projects", []))
        }
    }
