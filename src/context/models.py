from datetime import datetime, UTC
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field as SQLField, Column, JSON
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    session_id: UUID = SQLField(foreign_key="researchsession.id")
    description: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(UTC))
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = SQLField(default=None, sa_column=Column(JSON))


class Checkpoint(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    session_id: UUID = SQLField(foreign_key="researchsession.id")
    timestamp: datetime = SQLField(default_factory=lambda: datetime.now(UTC))
    task_id: Optional[UUID] = None
    tool_id: Optional[str] = None
    state_snapshot: Dict[str, Any] = SQLField(sa_column=Column(JSON))


class ResearchSession(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    query: str
    status: str = "running"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    rolling_summary: str = ""
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = SQLField(default_factory=lambda: datetime.now(UTC))
    metadata_json: Dict[str, Any] = SQLField(default_factory=dict, sa_column=Column(JSON))

# For Pydantic-only models used in communication
class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
