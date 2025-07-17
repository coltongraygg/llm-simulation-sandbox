from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db, Scenario, Run
from schemas import ScenarioCreate, ScenarioResponse, RunResponse, RunSummary

router = APIRouter()

# Scenario endpoints
@router.get("/scenarios", response_model=List[ScenarioResponse])
async def get_scenarios(db: Session = Depends(get_db)):
    """Get all saved scenario definitions"""
    scenarios = db.query(Scenario).order_by(Scenario.created_at.desc()).all()
    return scenarios

@router.post("/scenarios", response_model=ScenarioResponse)
async def create_scenario(scenario: ScenarioCreate, db: Session = Depends(get_db)):
    """Create or update a scenario"""
    # Convert Pydantic models to dict for JSON storage
    participants_dict = [participant.dict() for participant in scenario.participants]
    settings_dict = scenario.settings.dict()
    
    db_scenario = Scenario(
        name=scenario.name,
        participants=participants_dict,
        system_prompt=scenario.system_prompt,
        settings=settings_dict
    )
    
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    
    return db_scenario

# Run endpoints
@router.get("/runs", response_model=List[RunSummary])
async def get_runs(db: Session = Depends(get_db)):
    """Get all past simulation runs (basic metadata)"""
    runs = db.query(Run).join(Scenario).order_by(Run.timestamp.desc()).all()
    
    # Create response with scenario names
    run_summaries = []
    for run in runs:
        run_summary = RunSummary(
            id=run.id,
            scenario_id=run.scenario_id,
            timestamp=run.timestamp,
            starred=run.starred,
            scenario_name=run.scenario.name if run.scenario else None
        )
        run_summaries.append(run_summary)
    
    return run_summaries

@router.get("/runs/{run_id}", response_model=RunResponse)
async def get_run(run_id: str, db: Session = Depends(get_db)):
    """Get full details of a specific run"""
    try:
        # Convert string to UUID for database query
        run_uuid = uuid.UUID(run_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid run ID format")
    
    run = db.query(Run).filter(Run.id == run_uuid).first()
    
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    return run 