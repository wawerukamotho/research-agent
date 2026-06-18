from typing import Any, Dict, List
from registry.pipeline import ToolPipeline
from tools.search.models import SearchResponse
from tools.fetch.models import BatchFetchResponse, FetchedDocument
from tools.analyze.models import ClaimListResponse, VerifiedClaimListResponse
from tools.write.models import WriteResponse

def create_research_pipeline() -> ToolPipeline:
    pipeline = ToolPipeline("standard_research_flow")

    # 1. Search (Input: query -> Output: SearchResponse)
    pipeline.add_step("search.web_search")

    # 2. Fetch (Input: SearchResponse -> BatchFetchInput -> Output: BatchFetchResponse)
    def search_to_fetch(search_res: SearchResponse) -> Dict[str, Any]:
        urls = [res.url for res in search_res.results]
        return {"urls": urls}
    pipeline.add_step("fetch.batch_fetch", input_mapper=search_to_fetch)

    # 3. Extract Claims (Input: BatchFetchResponse -> AnalysisInput -> Output: ClaimListResponse)
    def fetch_to_extract(fetch_res: BatchFetchResponse) -> Dict[str, Any]:
        return {"documents": fetch_res.documents}
    pipeline.add_step("analyze.extract_claims", input_mapper=fetch_to_extract)

    # 4. Cross Reference (Input: ClaimListResponse -> AnalysisInput -> Output: VerifiedClaimListResponse)
    def extract_to_verify(claim_res: ClaimListResponse) -> Dict[str, Any]:
        return {"claims": claim_res.claims}
    pipeline.add_step("analyze.cross_reference_claims", input_mapper=extract_to_verify)

    # 5. Draft (Input: VerifiedClaimListResponse -> WriteInput -> Output: WriteResponse)
    def verify_to_draft(verified_res: VerifiedClaimListResponse) -> Dict[str, Any]:
        return {
            "prompt": "Draft a section based on these verified claims.",
            "verified_claims": verified_res.verified_claims
        }
    pipeline.add_step("write.draft_section", input_mapper=verify_to_draft)

    return pipeline
