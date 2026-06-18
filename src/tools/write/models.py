from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Citation(BaseModel):
    id: str
    text: str
    url: Optional[str] = None
    source: Optional[str] = None

class ReportSection(BaseModel):
    title: str
    content: str
    citations: List[Citation] = Field(default_factory=list)
    subsections: List['ReportSection'] = Field(default_factory=list)

class ExecutiveSummary(BaseModel):
    summary: str
    key_findings: List[str]
    confidence_score: float

class ResearchReport(BaseModel):
    title: str
    executive_summary: ExecutiveSummary
    sections: List[ReportSection]
    bibliography: List[Citation]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SectionBrief(BaseModel):
    title: str
    objectives: List[str]
    context: Optional[str] = None

class Outline(BaseModel):
    title: str
    sections: List[SectionBrief]

class WriteInput(BaseModel):
    prompt: str
    context: Optional[str] = None
    params: Dict[str, Any] = Field(default_factory=dict)

class AssembleReportInput(BaseModel):
    title: str
    executive_summary: ExecutiveSummary
    sections: List[ReportSection]
    bibliography: List[Citation]

class WriteResponse(BaseModel):
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class OutlineResponse(BaseModel):
    outline: Outline

class ReportResponse(BaseModel):
    report: ResearchReport
