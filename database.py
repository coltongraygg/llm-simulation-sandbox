from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Text, JSON, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from datetime import datetime
import json

# Database configuration
DATABASE_URL = "sqlite:///./driftwood.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    participants = Column(JSON, nullable=False)  # List of participant objects
    system_prompt = Column(Text, nullable=False)
    settings = Column(JSON, nullable=False)  # Model settings (temperature, max_tokens, etc.)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to runs
    runs = relationship("Run", back_populates="scenario")

class Run(Base):
    __tablename__ = "runs"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4, index=True)
    scenario_id = Column(UUID, ForeignKey("scenarios.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    starred = Column(Boolean, default=False)
    log = Column(JSON, nullable=False)  # Conversation log array
    
    # Relationship to scenario
    scenario = relationship("Scenario", back_populates="runs")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine) 