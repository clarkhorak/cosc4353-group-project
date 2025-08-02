from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
import os

# Create database URL from Supabase connection string
def get_database_url():
    if settings.database_url:
        return settings.database_url
    else:
        raise ValueError("DATABASE_URL not configured")

# Create SQLAlchemy engine (lazy creation)
def get_engine():
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Create SessionLocal class
def get_session_local():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def create_tables():
    from .models.database import Base
    engine = get_engine()
    Base.metadata.create_all(bind=engine) 