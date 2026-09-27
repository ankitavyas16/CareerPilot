"""CareerPilot AI - Main FastAPI Application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.db.database import init_db
from app.routes import profile, jobs, applications, analysis

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle events."""
    init_db()
    yield

app = FastAPI(
    title="CareerPilot AI",
    description="Personal AI Career Agent for Job Search, Resume Matching, and Interview Prep",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "CareerPilot AI"}

# Mount functional routers
app.include_router(profile.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(analysis.router)  # Add this line

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to CareerPilot AI API",
        "docs": "/docs",
        "health": "/health",
    }
