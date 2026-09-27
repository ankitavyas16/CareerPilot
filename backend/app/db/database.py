"""Database setup and session management."""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

Base = declarative_base()

connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """FastAPI dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Import all models and create all database tables."""
    # Importing models registers them with Base.metadata
    import app.models.user  # noqa: F401
    import app.models.job  # noqa: F401
    import app.models.application  # noqa: F401
    import app.models.interview  # noqa: F401

    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized successfully")

def clear_db():
    """Drop all tables."""
    import app.models.user  # noqa: F401
    import app.models.job  # noqa: F401
    import app.models.application  # noqa: F401
    import app.models.interview  # noqa: F401

    Base.metadata.drop_all(bind=engine)
    print("✓ Database cleared")

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    if "sqlite" in settings.database_url:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
