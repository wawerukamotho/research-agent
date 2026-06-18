from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

class SearchQuery(BaseModel):
    query: str
    limit: int = Field(default=10, ge=1, le=50)
    offset: int = Field(default=0, ge=0)
    extra_params: Dict[str, Any] = Field(default_factory=dict)

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    score: Optional[float] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_count: Optional[int] = None
