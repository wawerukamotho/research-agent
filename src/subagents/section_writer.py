from typing import List, Optional
from pydantic import BaseModel
from subagents.base import BaseSubagent
from tools.write.models import SectionBrief, ReportSection

class SectionWriterInput(BaseModel):
    brief: SectionBrief

class SectionWriterOutput(BaseModel):
    section: ReportSection

class SectionWriterSubagent(BaseSubagent):
    def __init__(self):
        scope = [
            "write.draft_section",
            "write.format_citation",
            "write.add_inline_citation",
            "analyze.summarize_text"
        ]
        super().__init__(name="SectionWriter", scope=scope)

    async def run(self, input_data: SectionWriterInput) -> SectionWriterOutput:
        # Mock logic:
        # 1. Summarize context
        # 2. Draft section
        # 3. Add citations

        section = ReportSection(
            title=input_data.brief.title,
            content=f"Content for {input_data.brief.title} drafted by specialized subagent.",
            citations=[]
        )
        return SectionWriterOutput(section=section)
