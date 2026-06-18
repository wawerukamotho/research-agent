from typing import Any, Dict, List
from registry.base import BaseTool
from registry.decorator import tool
from tools.analyze.models import (
    AnalysisInput, ComparisonInput, AnalysisResponse, ClaimListResponse,
    VerifiedClaimListResponse, SourceScoreListResponse, CoverageReport,
    EntityListResponse, TimelineResponse, Claim, VerifiedClaim, Entity,
    TimelineEvent, SourceScore
)
from tools.analyze.provider import LLMAnalysisProvider

_provider = LLMAnalysisProvider()

@tool(
    name="summarize_text",
    namespace="analyze",
    description="Generate a concise summary of the provided text.",
    input_schema=AnalysisInput,
    output_schema=AnalysisResponse
)
class SummarizeTextTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> AnalysisResponse:
        return await _provider.analyze(input_data.text, "Summarize the text.", AnalysisResponse, input_data.context)

@tool(
    name="extract_claims",
    namespace="analyze",
    description="Extract verifiable claims from the text.",
    input_schema=AnalysisInput,
    output_schema=ClaimListResponse
)
class ExtractClaimsTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> ClaimListResponse:
        return await _provider.analyze(input_data.text, "Extract verifiable claims.", ClaimListResponse, input_data.context)

@tool(
    name="cross_reference_claims",
    namespace="analyze",
    description="Cross-reference claims against multiple sources.",
    input_schema=AnalysisInput,
    output_schema=VerifiedClaimListResponse
)
class CrossReferenceClaimsTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> VerifiedClaimListResponse:
        return await _provider.analyze(input_data.text, "Cross-reference and verify claims.", VerifiedClaimListResponse, input_data.context)

@tool(
    name="score_source_credibility",
    namespace="analyze",
    description="Evaluate the credibility of sources based on provided evidence.",
    input_schema=AnalysisInput,
    output_schema=SourceScoreListResponse
)
class ScoreSourceCredibilityTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> SourceScoreListResponse:
        return await _provider.analyze(input_data.text, "Score the credibility of sources.", SourceScoreListResponse, input_data.context)

@tool(
    name="detect_contradictions",
    namespace="analyze",
    description="Identify contradictory information across different sources.",
    input_schema=AnalysisInput,
    output_schema=VerifiedClaimListResponse
)
class DetectContradictionsTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> VerifiedClaimListResponse:
        return await _provider.analyze(input_data.text, "Identify contradictions.", VerifiedClaimListResponse, input_data.context)

@tool(
    name="extract_entities",
    namespace="analyze",
    description="Extract key entities (people, organizations, locations) from the text.",
    input_schema=AnalysisInput,
    output_schema=EntityListResponse
)
class ExtractEntitiesTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> EntityListResponse:
        return await _provider.analyze(input_data.text, "Extract key entities.", EntityListResponse, input_data.context)

@tool(
    name="compute_topic_coverage",
    namespace="analyze",
    description="Analyze how well the research covers the target topics.",
    input_schema=AnalysisInput,
    output_schema=CoverageReport
)
class ComputeTopicCoverageTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> CoverageReport:
        return await _provider.analyze(input_data.text, "Compute topic coverage.", CoverageReport, input_data.context)

@tool(
    name="rank_sources",
    namespace="analyze",
    description="Rank sources based on relevance and quality.",
    input_schema=AnalysisInput,
    output_schema=SourceScoreListResponse
)
class RankSourcesTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> SourceScoreListResponse:
        return await _provider.analyze(input_data.text, "Rank sources.", SourceScoreListResponse, input_data.context)

@tool(
    name="identify_knowledge_gaps",
    namespace="analyze",
    description="Identify areas where information is missing or insufficient.",
    input_schema=AnalysisInput,
    output_schema=CoverageReport
)
class IdentifyKnowledgeGapsTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> CoverageReport:
        return await _provider.analyze(input_data.text, "Identify knowledge gaps.", CoverageReport, input_data.context)

@tool(
    name="classify_claim_type",
    namespace="analyze",
    description="Classify claims into categories (factual, opinion, causal, etc.).",
    input_schema=AnalysisInput,
    output_schema=ClaimListResponse
)
class ClassifyClaimTypeTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> ClaimListResponse:
        return await _provider.analyze(input_data.text, "Classify claim types.", ClaimListResponse, input_data.context)

@tool(
    name="timeline_extract",
    namespace="analyze",
    description="Extract a chronological timeline of events from the text.",
    input_schema=AnalysisInput,
    output_schema=TimelineResponse
)
class TimelineExtractTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> TimelineResponse:
        return await _provider.analyze(input_data.text, "Extract timeline of events.", TimelineResponse, input_data.context)

@tool(
    name="sentiment_analysis",
    namespace="analyze",
    description="Analyze the sentiment and tone of the text.",
    input_schema=AnalysisInput,
    output_schema=AnalysisResponse
)
class SentimentAnalysisTool(BaseTool):
    async def run(self, input_data: AnalysisInput) -> AnalysisResponse:
        return await _provider.analyze(input_data.text, "Analyze sentiment and tone.", AnalysisResponse, input_data.context)

@tool(
    name="compare_sources",
    namespace="analyze",
    description="Compare multiple sources for consistency and differences.",
    input_schema=ComparisonInput,
    output_schema=AnalysisResponse
)
class CompareSourcesTool(BaseTool):
    async def run(self, input_data: ComparisonInput) -> AnalysisResponse:
        combined_text = "\n---\n".join(input_data.texts)
        return await _provider.analyze(combined_text, f"Compare these sources based on: {input_data.criteria or 'general consistency'}", AnalysisResponse)
