from typing import Any, Dict, List
from registry.base import BaseTool
from registry.decorator import tool
from tools.write.models import (
    WriteInput, WriteResponse, OutlineResponse, ReportResponse,
    AssembleReportInput, ResearchReport, ReportSection, Citation,
    ExecutiveSummary, Outline
)
from tools.write.provider import LLMWriteProvider

_provider = LLMWriteProvider()

@tool(
    name="draft_section",
    namespace="write",
    description="Draft a specific section of the research report.",
    input_schema=WriteInput,
    output_schema=WriteResponse
)
class DraftSectionTool(BaseTool):
    async def run(self, input_data: WriteInput) -> WriteResponse:
        return await _provider.generate(input_data.prompt, "Draft a report section.", WriteResponse, input_data.context)

@tool(
    name="write_introduction",
    namespace="write",
    description="Write the introduction for the research report.",
    input_schema=WriteInput,
    output_schema=WriteResponse
)
class WriteIntroductionTool(BaseTool):
    async def run(self, input_data: WriteInput) -> WriteResponse:
        return await _provider.generate(input_data.prompt, "Write report introduction.", WriteResponse, input_data.context)

@tool(
    name="write_conclusion",
    namespace="write",
    description="Write the conclusion for the research report.",
    input_schema=WriteInput,
    output_schema=WriteResponse
)
class WriteConclusionTool(BaseTool):
    async def run(self, input_data: WriteInput) -> WriteResponse:
        return await _provider.generate(input_data.prompt, "Write report conclusion.", WriteResponse, input_data.context)

@tool(
    name="format_citation",
    namespace="write",
    description="Format a citation according to a specific style.",
    input_schema=WriteInput,
    output_schema=WriteResponse
)
class FormatCitationTool(BaseTool):
    async def run(self, input_data: WriteInput) -> WriteResponse:
        return await _provider.generate(input_data.prompt, "Format citation.", WriteResponse, input_data.context)

@tool(
    name="assemble_report",
    namespace="write",
    description="Assemble all sections into a final research report.",
    input_schema=AssembleReportInput,
    output_schema=ReportResponse
)
class AssembleReportTool(BaseTool):
    async def run(self, input_data: AssembleReportInput) -> ReportResponse:
        report = ResearchReport(
            title=input_data.title,
            executive_summary=input_data.executive_summary,
            sections=input_data.sections,
            bibliography=input_data.bibliography
        )
        return ReportResponse(report=report)

@tool(
    name="add_inline_citation",
    namespace="write",
    description="Add inline citations to a text section.",
    input_schema=WriteInput,
    output_schema=WriteResponse
)
class AddInlineCitationTool(BaseTool):
    async def run(self, input_data: WriteInput) -> WriteResponse:
        return await _provider.generate(input_data.prompt, "Add inline citations.", WriteResponse, input_data.context)

@tool(
    name="generate_executive_summary",
    namespace="write",
    description="Generate an executive summary based on report content.",
    input_schema=WriteInput,
    output_schema=WriteResponse
)
class GenerateExecutiveSummaryTool(BaseTool):
    async def run(self, input_data: WriteInput) -> WriteResponse:
        return await _provider.generate(input_data.prompt, "Generate executive summary.", WriteResponse, input_data.context)

@tool(
    name="export_markdown",
    namespace="write",
    description="Export the research report to Markdown format.",
    input_schema=ReportResponse,
    output_schema=WriteResponse
)
class ExportMarkdownTool(BaseTool):
    async def run(self, input_data: ReportResponse) -> WriteResponse:
        report = input_data.report
        md = f"# {report.title}\n\n"
        md += f"## Executive Summary\n{report.executive_summary.summary}\n\n"
        for section in report.sections:
            md += f"## {section.title}\n{section.content}\n\n"
        md += "## Bibliography\n"
        for cite in report.bibliography:
            md += f"- {cite.text} ({cite.url})\n"
        return WriteResponse(content=md)

@tool(
    name="export_json",
    namespace="write",
    description="Export the research report to JSON format.",
    input_schema=ReportResponse,
    output_schema=WriteResponse
)
class ExportJsonTool(BaseTool):
    async def run(self, input_data: ReportResponse) -> WriteResponse:
        return WriteResponse(content=input_data.report.model_dump_json())

@tool(
    name="create_outline",
    namespace="write",
    description="Create an outline for the research report.",
    input_schema=WriteInput,
    output_schema=OutlineResponse
)
class CreateOutlineTool(BaseTool):
    async def run(self, input_data: WriteInput) -> OutlineResponse:
        return await _provider.generate(input_data.prompt, "Create report outline.", OutlineResponse, input_data.context)

@tool(
    name="suggest_followup_questions",
    namespace="write",
    description="Suggest follow-up questions for further research.",
    input_schema=WriteInput,
    output_schema=WriteResponse
)
class SuggestFollowupQuestionsTool(BaseTool):
    async def run(self, input_data: WriteInput) -> WriteResponse:
        return await _provider.generate(input_data.prompt, "Suggest follow-up questions.", WriteResponse, input_data.context)

@tool(
    name="validate_report_structure",
    namespace="write",
    description="Validate the logical structure of the research report.",
    input_schema=ReportResponse,
    output_schema=WriteResponse
)
class ValidateReportStructureTool(BaseTool):
    async def run(self, input_data: ReportResponse) -> WriteResponse:
        prompt = f"Validate this report: {input_data.report.title}"
        return await _provider.generate(prompt, "Validate report structure.", WriteResponse)
