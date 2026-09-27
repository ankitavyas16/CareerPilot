"""Pytest fixtures for database and API client."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import get_db
from app.models.user import Base as UserBase
from app.models.job import Base as JobBase
from app.models.application import Base as ApplicationBase
from app.models.interview import Base as InterviewBase

# Isolated in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a pristine database for each test."""
    UserBase.metadata.create_all(bind=engine)
    JobBase.metadata.create_all(bind=engine)
    ApplicationBase.metadata.create_all(bind=engine)
    InterviewBase.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        UserBase.metadata.drop_all(bind=engine)
        JobBase.metadata.drop_all(bind=engine)
        ApplicationBase.metadata.drop_all(bind=engine)
        InterviewBase.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
