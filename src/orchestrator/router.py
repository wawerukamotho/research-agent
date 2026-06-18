from fastapi import APIRouter, BackgroundTasks, HTTPException
from uuid import UUID
from typing import Dict
from orchestrator.models import ResearchRequest, ResearchStatus
from orchestrator.engine import Orchestrator

router = APIRouter(prefix="/research", tags=["research"])

# Simple in-memory store for active orchestrators
_active_jobs: Dict[UUID, Orchestrator] = {}

@router.post("/", response_model=ResearchStatus)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    orchestrator = Orchestrator(request)
    _active_jobs[orchestrator.session_manager.session.id] = orchestrator

    # Run in background
    background_tasks.add_task(orchestrator.run)

    return await orchestrator.get_status()

@router.get("/{session_id}", response_model=ResearchStatus)
async def get_research_status(session_id: UUID):
    if session_id not in _active_jobs:
        raise HTTPException(status_code=404, detail="Research job not found")

    return await _active_jobs[session_id].get_status()
