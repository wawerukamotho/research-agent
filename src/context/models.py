from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    description: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None


class Checkpoint(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    task_id: Optional[UUID] = None
    tool_id: Optional[str] = None
    state_snapshot: Dict[str, Any]


class SourceRegistry(BaseModel):
    sources: List[Dict[str, Any]] = Field(default_factory=list)


class ResearchPlan(BaseModel):
    objectives: List[str]
    tasks: List[Task] = Field(default_factory=list)
    completed_tasks: List[UUID] = Field(default_factory=list)
    checkpoints: List[Checkpoint] = Field(default_factory=list)
    source_registry: SourceRegistry = Field(default_factory=SourceRegistry)


class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0


class ResearchSession(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    query: str
    plan: ResearchPlan
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    rolling_summary: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
