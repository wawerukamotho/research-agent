from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from context.models import TaskStatus

class ResearchRequest(BaseModel):
    query: str
    max_steps: int = Field(default=20, ge=1, le=50)
    budget_limit: float = Field(default=5.0, ge=0.01)

class ResearchStatus(BaseModel):
    session_id: UUID
    query: str
    status: str
    progress: float
    current_task: Optional[str] = None
    step_count: int
    created_at: datetime
    updated_at: datetime

class OrchestratorEvent(BaseModel):
    session_id: UUID
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
