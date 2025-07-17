from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db, Scenario, Run
from schemas import ScenarioCreate, ScenarioResponse, RunResponse, RunSummary, StarUpdateRequest
from simulation import simulation_engine

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

@router.post("/run", response_model=RunResponse)
async def run_simulation(scenario_id: str, db: Session = Depends(get_db)):
    """Run a simulation based on a scenario and return the conversation log"""
    try:
        # Convert string to UUID
        scenario_uuid = uuid.UUID(scenario_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid scenario ID format")
    
    # Get the scenario
    scenario = db.query(Scenario).filter(Scenario.id == scenario_uuid).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    try:
        # Run the simulation
        conversation_log = await simulation_engine.run_simulation(
            participants=scenario.participants,
            system_prompt=scenario.system_prompt,
            settings=scenario.settings
        )
        
        # Save the run to database
        db_run = Run(
            scenario_id=scenario.id,
            log=conversation_log
        )
        
        db.add(db_run)
        db.commit()
        db.refresh(db_run)
        
        return db_run
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@router.patch("/runs/{run_id}/star", response_model=RunResponse)
async def toggle_star(run_id: str, star_request: StarUpdateRequest, db: Session = Depends(get_db)):
    """Toggle the starred status of a simulation run"""
    try:
        # Convert string to UUID
        run_uuid = uuid.UUID(run_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid run ID format")
    
    # Get the run
    run = db.query(Run).filter(Run.id == run_uuid).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    # Update starred status
    run.starred = star_request.starred
    db.commit()
    db.refresh(run)
    
    return run

@router.delete("/runs/{run_id}")
async def delete_run(run_id: str, db: Session = Depends(get_db)):
    """Delete a specific simulation run"""
    try:
        # Convert string to UUID
        run_uuid = uuid.UUID(run_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid run ID format")
    
    # Get the run
    run = db.query(Run).filter(Run.id == run_uuid).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    # Delete the run
    db.delete(run)
    db.commit()
    
    return {"message": "Run deleted successfully"}

@router.delete("/runs")
async def delete_all_unstarred_runs(db: Session = Depends(get_db)):
    """Delete all simulation runs except starred ones"""
    # Delete only unstarred runs
    deleted_count = db.query(Run).filter(Run.starred == False).delete()
    db.commit()
    
    return {"message": f"Deleted {deleted_count} unstarred runs", "deleted_count": deleted_count} 