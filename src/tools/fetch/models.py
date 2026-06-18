from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class FetchInput(BaseModel):
    url: str
    params: Dict[str, Any] = Field(default_factory=dict)

class BatchFetchInput(BaseModel):
    urls: List[str]

class FetchedDocument(BaseModel):
    url: str
    content: str
    content_type: str = "text/html"
    title: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    raw_content: Optional[bytes] = None

    model_config = {
        "arbitrary_types_allowed": True
    }

class FetchResponse(BaseModel):
    document: FetchedDocument

class BatchFetchResponse(BaseModel):
    documents: List[FetchedDocument]
