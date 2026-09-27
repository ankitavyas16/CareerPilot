# CareerPilot AI 🚀

**Personal AI Career Agent for Job Search, Resume Matching, and Interview Preparation**

CareerPilot AI is a production-grade full-stack application that helps you manage your job search, analyze job descriptions, identify skill gaps, match jobs to your profile, track applications, and prepare for interviews—all powered by AI.

---

## 🎯 Features

### Core Capabilities

✅ **User Profile & Career Memory**
- Store your career history, skills, experience, education, and projects
- Maintain multiple resume versions
- Set target roles, preferred locations, and salary expectations
- Track learning goals

✅ **Job Description Analyzer**
- Paste any job posting and extract structured data
- Automatically identifies required/preferred skills
- Extracts technologies, responsibilities, and keywords
- Generates ATS-friendly keywords

✅ **Intelligent Job Matching**
- Transparent matching algorithm (0-100%)
- Shows matching vs. missing skills
- Evaluates experience fit and work mode alignment
- Provides clear recommendations (apply/learn first/skip)
- Batch job matching with ranked results

✅ **Application Tracker**
- Track job applications through full pipeline
- Statuses: saved → applied → screening → interview → offer/rejected
- Store recruiter contact info and interview dates
- Notes and follow-up reminders

✅ **Interview Preparation**
- AI-generated technical, behavioral, and company-specific questions
- Practice question tracking
- Interview feedback and outcome logging
- STAR story bank for behavioral prep

✅ **Daily Career Briefing**
- Morning dashboard with key metrics
- In-demand skills appearing across tracked jobs
- Pending interviews and follow-ups
- Personalized learning recommendations

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or newer
- pip and virtualenv
- Git

### Installation

1. **Clone the repository:**

	```bash
	git clone https://github.com/yourusername/careerpilot-ai.git
	cd careerpilot-ai
	```

## 🏗️ Architecture

### Tech Stack

**Backend:**
- **FastAPI** - Modern, fast REST API framework
- **SQLAlchemy** - ORM for database models
- **SQLite** (development) / PostgreSQL (production)
- **OpenAI API** - LLM integration for AI features
- **Pydantic** - Data validation & schema generation

**Frontend:**
- Vanilla **HTML5, CSS3, JavaScript** (no build step required)
- Responsive design with modern CSS Grid/Flexbox
- CORS-enabled for API integration

**Development & Testing:**
- **pytest** - Unit & integration testing
- **Uvicorn** - ASGI server
- **Python 3.12+**

### Project Structure

careerpilot-ai/ ├── backend/ │ ├── app/ │ │ ├── main.py # FastAPI app entry point │ │ ├── config.py # Environment configuration │ │ ├── models/ # SQLAlchemy models │ │ │ ├── user.py │ │ │ ├── job.py │ │ │ ├── application.py │ │ │ └── interview.py │ │ ├── schemas/ # Pydantic request/response schemas │ │ ├── routes/ # API endpoint routers │ │ │ ├── profile.py │ │ │ ├── jobs.py │ │ │ ├── applications.py │ │ │ └── analysis.py │ │ ├── db/ # Database setup │ │ │ ├── database.py │ │ │ └── seed.py │ │ ├── tools/ # AI tools & services │ │ │ └── llm_service.py │ │ └── utils/ # Utilities │ ├── tests/ # Pytest test suite │ ├── requirements.txt │ ├── pytest.ini │ └── .env.example ├── frontend/ │ ├── index.html # Main dashboard │ ├── css/ │ │ ├── style.css # Core styles │ │ └── dashboard.css # Dashboard-specific styles │ └── js/ │ ├── app.js # Main app logic │ └── api.js # API client ├── docs/ │ ├── API.md │ ├── ARCHITECTURE.md │ └── DATABASE_SCHEMA.md ├── .gitignore ├── .env.example └── README.md

