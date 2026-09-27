"""Integration tests for FastAPI endpoints."""

def test_health_check(client):
    """Ensure the service returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_and_get_user(client):
    """Test user profile creation and retrieval."""
    payload = {
        "name": "Morgan Taylor",
        "email": "morgan@example.com",
        "current_role": "Data Analyst",
        "years_experience": 2.5,
        "target_roles": ["Data Scientist"],
        "preferred_locations": ["Chicago, IL"],
        "preferred_work_mode": "hybrid",
        "learning_goals": ["PyTorch"],
    }
    post_res = client.post("/profile", json=payload)
    assert post_res.status_code == 201

    get_res = client.get("/profile")
    assert get_res.status_code == 200
    profile = get_res.json()
    assert profile["email"] == "morgan@example.com"
    assert profile["years_experience"] == 2.5

def test_jobs_flow(client):
    """Test creating and retrieving jobs."""
    job_payload = {
        "title": "Machine Learning Engineer",
        "company": "Cognitive AI",
        "description": "Looking for Python, Scikit-Learn, and FastAPI experience.",
        "location": "Remote",
        "work_mode": "remote",
    }
    create_res = client.post("/jobs", json=job_payload)
    assert create_res.status_code == 201

    list_res = client.get("/jobs")
    assert list_res.status_code == 200
    jobs = list_res.json()
    assert len(jobs) >= 1
    assert jobs[0]["company"] == "Cognitive AI"
