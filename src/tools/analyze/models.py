from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from tools.fetch.models import FetchedDocument

class AnalysisInput(BaseModel):
    text: Optional[str] = None
    documents: Optional[List[FetchedDocument]] = None
    claims: Optional[List['Claim']] = None
    context: Optional[str] = None
    params: Dict[str, Any] = Field(default_factory=dict)

class ComparisonInput(BaseModel):
    texts: List[str]
    criteria: Optional[str] = None

class Claim(BaseModel):
    claim: str
    source: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)
    category: Optional[str] = None

class VerifiedClaim(BaseModel):
    claim: str
    verdict: Literal["verified", "contradicted", "unverified", "partially_verified"]
    evidence: List[str]
    confidence: float
    sources: List[str]

class Entity(BaseModel):
    name: str
    type: str
    description: Optional[str] = None

class TimelineEvent(BaseModel):
    date: str
    event: str
    importance: float = Field(ge=0.0, le=1.0)

class SourceScore(BaseModel):
    source_url: str
    credibility_score: float = Field(ge=0.0, le=1.0)
    reasons: List[str]

class CoverageReport(BaseModel):
    topics_covered: List[str]
    missing_topics: List[str]
    coverage_percentage: float

class AnalysisResponse(BaseModel):
    summary: Optional[str] = None
    claims: Optional[List[Claim]] = None
    entities: Optional[List[Entity]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ClaimListResponse(BaseModel):
    claims: List[Claim]

class VerifiedClaimListResponse(BaseModel):
    verified_claims: List[VerifiedClaim]

class EntityListResponse(BaseModel):
    entities: List[Entity]

class TimelineResponse(BaseModel):
    events: List[TimelineEvent]

class SourceScoreListResponse(BaseModel):
    scores: List[SourceScore]
