from fastapi import APIRouter, BackgroundTasks, HTTPException, Response, Request
from fastapi.responses import StreamingResponse
from uuid import UUID
from typing import Dict, Literal, AsyncGenerator
import json
import asyncio
from orchestrator.models import ResearchRequest, ResearchStatus
from orchestrator.engine import Orchestrator

router = APIRouter(prefix="/research", tags=["research"])

# Research job registry relies on persistent state
@router.post("", response_model=ResearchStatus)
@router.post("/", response_model=ResearchStatus)
async def start_research(request: Request, research_request: ResearchRequest, background_tasks: BackgroundTasks):
    orchestrator = Orchestrator(
        research_request,
        redis_client=request.app.state.redis,
        db_engine=request.app.state.db_engine
    )
    # Persist session immediately
    await orchestrator.session_manager.save()

    # Run in background
    background_tasks.add_task(orchestrator.run)

    return await orchestrator.get_status()

@router.get("/{session_id}", response_model=ResearchStatus)
async def get_research_status(request: Request, session_id: UUID):
    # Try resume from database
    try:
        orchestrator = Orchestrator(
            request=ResearchRequest(query=""),
            redis_client=request.app.state.redis,
            db_engine=request.app.state.db_engine
        )
        orchestrator.session_manager = await ResearchSessionManager.resume(
            session_id,
            db_engine=request.app.state.db_engine
        )
        return await orchestrator.get_status()
    except Exception:
        raise HTTPException(status_code=404, detail="Research job not found")

@router.get("/{session_id}/download/{format}")
async def download_report(request: Request, session_id: UUID, format: Literal["md", "json", "pdf", "docx"]):
    try:
        orchestrator = Orchestrator(
            request=ResearchRequest(query=""),
            redis_client=request.app.state.redis,
            db_engine=request.app.state.db_engine
        )
        orchestrator.session_manager = await ResearchSessionManager.resume(
            session_id,
            db_engine=request.app.state.db_engine
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Research job not found")
    from tools.write.models import ReportResponse, ResearchReport, ExecutiveSummary

    report = ResearchReport(
        title=orchestrator.request.query,
        executive_summary=ExecutiveSummary(summary="...", key_findings=[], confidence_score=0.9),
        sections=[],
        bibliography=[]
    )
    report_res = ReportResponse(report=report)

    from registry.registry import registry
    tool_id = f"write.export_{format}"
    result = await registry.execute(tool_id, {"input_data": report_res})

    import base64
    if format in ["pdf", "docx"]:
        content = base64.b64decode(result.content)
    else:
        content = result.content.encode('utf-8')

    media_types = {
        "md": "text/markdown",
        "json": "application/json",
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }

    return Response(
        content=content,
        media_type=media_types[format],
        headers={"Content-Disposition": f"attachment; filename=report.{format}"}
    )

@router.get("/{session_id}/events")
async def event_stream(session_id: UUID, request: Request):
    if session_id not in _active_jobs:
        raise HTTPException(status_code=404, detail="Research job not found")

    orchestrator = _active_jobs[session_id]

    async def event_generator() -> AsyncGenerator[str, None]:
        last_step = -1
        while True:
            if await request.is_disconnected():
                break

            status = await orchestrator.get_status()
            if status.step_count > last_step:
                data = {
                    "event": "progress",
                    "data": status.model_dump(mode="json")
                }
                yield f"data: {json.dumps(data)}\n\n"
                last_step = status.step_count

            if status.status == "finished":
                yield f"data: {json.dumps({'event': 'completed', 'data': {}})}\n\n"
                break

            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
