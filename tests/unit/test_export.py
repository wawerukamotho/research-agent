import pytest
from tools.write.models import ResearchReport, ExecutiveSummary, ReportSection
from tools.write.export import generate_markdown, generate_pdf, generate_docx

@pytest.fixture
def mock_report():
    return ResearchReport(
        title="Test Report",
        executive_summary=ExecutiveSummary(
            summary="This is a summary",
            key_findings=["Finding 1"],
            confidence_score=0.9
        ),
        sections=[
            ReportSection(title="Section 1", content="Content 1")
        ],
        bibliography=[]
    )

def test_markdown_export(mock_report):
    md = generate_markdown(mock_report)
    assert "# Test Report" in md
    assert "## Executive Summary" in md
    assert "Section 1" in md

def test_pdf_export(mock_report):
    pdf_bytes = generate_pdf(mock_report)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0

def test_docx_export(mock_report):
    docx_bytes = generate_docx(mock_report)
    assert isinstance(docx_bytes, bytes)
    assert len(docx_bytes) > 0
