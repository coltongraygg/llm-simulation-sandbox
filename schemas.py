from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

class ParticipantModel(BaseModel):
    name: str
    role: str
    perspective: str
    meta_tags: List[str]

class SettingsModel(BaseModel):
    model: str = "gpt-4"
    temperature: float = Field(ge=0.0, le=2.0, default=0.7)
    max_tokens: int = Field(gt=0, default=400)

class ScenarioCreate(BaseModel):
    name: str
    participants: List[ParticipantModel]
    system_prompt: str
    settings: SettingsModel

class ScenarioResponse(BaseModel):
    id: uuid.UUID
    name: str
    participants: List[Dict[str, Any]]
    system_prompt: str
    settings: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

class RunResponse(BaseModel):
    id: uuid.UUID
    scenario_id: uuid.UUID
    timestamp: datetime
    starred: bool
    log: List[Dict[str, Any]]

    class Config:
        from_attributes = True

class RunSummary(BaseModel):
    id: uuid.UUID
    scenario_id: uuid.UUID
    timestamp: datetime
    starred: bool
    scenario_name: Optional[str] = None

    class Config:
        from_attributes = True 