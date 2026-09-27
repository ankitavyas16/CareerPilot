"""Database seeding script with realistic portfolio data."""
from datetime import datetime, timedelta
from app.db.database import SessionLocal, init_db
from app.models.user import User, Skill, Experience, Education, Project, Resume
from app.models.job import Job
from app.models.application import Application, InterviewPrep

def run_seed():
    """Seed the database with a complete candidate profile and sample jobs."""
    # Ensure all tables exist before inserting
    init_db()
    
    db = SessionLocal()
    try:
        # 1. Create or retrieve demo candidate
        user = db.query(User).filter(User.email == "alex.chen@example.com").first()
        if not user:
            user = User(
                name="Alex Chen",
                email="alex.chen@example.com",
                current_role="Data Analyst & Python Developer",
                years_experience=3.5,
                target_roles=["Machine Learning Engineer", "Data Scientist", "AI Engineer"],
                preferred_locations=["San Francisco, CA", "New York, NY", "Remote"],
                preferred_work_mode="hybrid",
                salary_min=115000,
                salary_max=155000,
                salary_currency="USD",
                learning_goals=[
                    "Master PyTorch and Transformer architectures",
                    "Deepen FastAPI asynchronous microservices patterns",
                    "MLOps pipelines with Docker and GitHub Actions"
                ],
                bio="Data Analyst transitioning into Machine Learning Engineering with 3+ years writing production Python, building analytical pipelines, and training predictive models."
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created demo user: {user.name} ({user.email})")

            # 2. Add Candidate Skills
            skills_data = [
                ("Python", "advanced", 3.5, 1),
                ("SQL", "advanced", 3.5, 1),
                ("FastAPI", "intermediate", 1.5, 1),
                ("Machine Learning", "intermediate", 2.0, 1),
                ("PyTorch", "beginner", 1.0, 0),
                ("Docker", "intermediate", 1.5, 1),
                ("PostgreSQL", "advanced", 3.0, 1),
                ("Pandas / NumPy", "advanced", 3.5, 1),
                ("Scikit-Learn", "intermediate", 2.0, 1),
                ("Git / CI/CD", "intermediate", 2.5, 1)
            ]
            for name, prof, yrs, ver in skills_data:
                db.add(Skill(
                    user_id=user.id,
                    name=name,
                    proficiency=prof,
                    years_experience=yrs,
                    verified=ver
                ))

            # 3. Add Work Experience
            db.add(Experience(
                user_id=user.id,
                company="Apex Metrics Corp",
                title="Data Analyst",
                start_date="2022-01",
                end_date=None,  # Current
                location="San Francisco, CA (Hybrid)",
                description="Designed analytical data flows and built customer churn prediction models.",
                responsibilities=[
                    "Engineered automated ETL pipelines using Python and PostgreSQL processing 1M+ daily events.",
                    "Built customer retention predictive model using Scikit-Learn yielding 83% precision.",
                    "Collaborated with product teams to design executive Tableau and Superset performance dashboards."
                ],
                achievements=[
                    "Reduced pipeline latency by 45% by rewriting legacy queries and indexing PostgreSQL tables.",
                    "Recognized with Q3 Technical Excellence Award for retention modeling."
                ]
            ))

            db.add(Experience(
                user_id=user.id,
                company="Beacon Tech Labs",
                title="Junior Python Developer",
                start_date="2020-07",
                end_date="2021-12",
                location="Remote",
                description="Backend API development and internal automation scripts.",
                responsibilities=[
                    "Maintained REST API endpoints built with FastAPI and SQLite.",
                    "Created automated test suites using pytest, boosting backend coverage from 45% to 82%."
                ],
                achievements=[
                    "Automated daily reporting routines saving approximately 6 hours of manual spreadsheet handling weekly."
                ]
            ))

            # 4. Add Education
            db.add(Education(
                user_id=user.id,
                school="University of California, Davis",
                degree="Bachelor of Science",
                field="Computer Science & Statistics",
                graduation_date="2020-06",
                description="Coursework: Data Structures, Applied Statistics, Database Management, Linear Algebra."
            ))

            # 5. Add Projects
            db.add(Project(
                user_id=user.id,
                name="CareerPilot AI Agent",
                description="Personal career co-pilot that evaluates job descriptions against user credentials and tracks interview pipelines.",
                url="https://github.com/example/careerpilot-ai",
                technologies=["FastAPI", "Python", "SQLAlchemy", "SQLite", "OpenAI API"],
                start_date="2024-01",
                end_date=None
            ))

            # 6. Add Base Resume
            db.add(Resume(
                user_id=user.id,
                name="Standard ML & Software Resume",
                content="Alex Chen | Python & ML Developer | Experienced in FastAPI, Scikit-Learn, SQL, and Docker.",
                keywords=["Python", "SQL", "FastAPI", "Machine Learning", "Docker", "Pandas"]
            ))

        # 7. Add Target Job Postings
        job_count = db.query(Job).count()
        if job_count == 0:
            sample_jobs = [
                Job(
                    title="Junior / Mid Machine Learning Engineer",
                    company="Novus Intelligence",
                    description=(
                        "Novus Intelligence is hiring a Machine Learning Engineer to deploy LLM applications "
                        "and tabular classifiers into production. Requirements: 2+ years of Python experience, "
                        "proficiency with FastAPI or Flask, practical experience with Scikit-Learn or PyTorch, "
                        "and solid SQL database skills. Nice to have: Docker, AWS, and MLOps deployment."
                    ),
                    url="https://careers.novusintel.example/jobs/ml-engineer-401",
                    experience_required="2-4 years",
                    location="San Francisco, CA",
                    work_mode="hybrid",
                    salary_min=120000,
                    salary_max=145000,
                    salary_currency="USD",
                    required_skills=["Python", "SQL", "FastAPI", "Machine Learning", "Scikit-Learn"],
                    preferred_skills=["Docker", "PyTorch", "MLOps", "AWS"],
                    technologies=["Python", "FastAPI", "PostgreSQL", "Docker", "PyTorch"],
                    key_responsibilities=[
                        "Develop and deploy ML microservices using FastAPI",
                        "Optimize inference pipelines and model latency",
                        "Collaborate with backend engineers to integrate APIs"
                    ],
                    keywords=["Python", "FastAPI", "Machine Learning", "PyTorch", "Docker"],
                    source="direct"
                ),
                Job(
                    title="Analytics Engineer",
                    company="Starlight FinTech",
                    description=(
                        "Starlight is looking for an Analytics Engineer to bridge raw data and production business logic. "
                        "Must have strong SQL mastery, Python data transformation experience (Pandas/dbt), "
                        "and familiarity with database modeling. Cloud data warehouse knowledge (Snowflake or BigQuery) preferred."
                    ),
                    url="https://starlightfintech.example/careers/analytics-eng",
                    experience_required="2-5 years",
                    location="Remote (US)",
                    work_mode="remote",
                    salary_min=110000,
                    salary_max=135000,
                    salary_currency="USD",
                    required_skills=["SQL", "Python", "Data Modeling", "Pandas"],
                    preferred_skills=["dbt", "Snowflake", "Docker"],
                    technologies=["SQL", "Python", "PostgreSQL", "Snowflake"],
                    key_responsibilities=[
                        "Design clean, maintainable analytical data transformations",
                        "Build monitoring checks for data accuracy and freshness",
                        "Partner with analytics and product stakeholders"
                    ],
                    keywords=["SQL", "Python", "Pandas", "Data Modeling", "ETL"],
                    source="direct"
                )
            ]
            for job in sample_jobs:
                db.add(job)
            db.commit()
            print(f"Added {len(sample_jobs)} sample job postings.")

        # 8. Add Sample Applications
        first_job = db.query(Job).first()
        if first_job and db.query(Application).count() == 0:
            app_entry = Application(
                user_id=user.id,
                job_id=first_job.id,
                company=first_job.company,
                role=first_job.title,
                job_url=first_job.url,
                status="interview",
                date_applied=datetime.utcnow() - timedelta(days=5),
                interview_date=datetime.utcnow() + timedelta(days=2),
                interview_type="Technical Video Screen (60m)",
                recruiter_name="Sarah Miller",
                recruiter_email="sarah.miller@novusintel.example",
                notes="Review FastAPI async routing and prepare STAR story on the churn prediction model."
            )
            db.add(app_entry)
            db.commit()
            db.refresh(app_entry)

            # Pre-populate interview prep notes
            prep_entry = InterviewPrep(
                application_id=app_entry.id,
                user_id=user.id,
                technical_questions=[
                    {"question": "How does FastAPI handle asynchronous request concurrency?", "answer": "FastAPI uses Starlette and asyncio underneath. Async def endpoints run directly on the main event loop.", "practiced": 1},
                    {"question": "What metrics do you use when evaluating imbalanced classification models?", "answer": "PR-AUC, F1-score, Precision, and Recall rather than standard accuracy.", "practiced": 2}
                ],
                behavioral_questions=[
                    {"question": "Tell me about a time you optimized a slow data pipeline.", "answer": "Walk through PostgreSQL query rewrite and indexing project at Apex Metrics.", "practiced": 1}
                ],
                jd_specific_questions=[
                    {"question": "How would you package and deploy a Scikit-Learn model behind a FastAPI microservice?", "answer": "Serialize via joblib, mount in Docker container with non-root user, expose POST /predict endpoint.", "practiced": 0}
                ],
                practice_count=4
            )
            db.add(prep_entry)
            db.commit()
            print("Added sample application and interview preparation tracking record.")

        print("✓ Seed completed successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
