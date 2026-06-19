from typing import List, Dict, Any
from pydantic import BaseModel

class EvalResult(BaseModel):
    benchmark_id: str
    grounding_score: float
    coverage_score: float
    citation_validity: float
    consistency_score: float

class Scorer:
    def calculate_coverage(self, actual_claims: List[str], expected_claims: List[str]) -> float:
        if not expected_claims:
            return 1.0

        matches = 0
        for expected in expected_claims:
            if any(expected.lower() in actual.lower() for actual in actual_claims):
                matches += 1
        return matches / len(expected_claims)

    def calculate_grounding(self, verified_claims_count: int, total_claims_count: int) -> float:
        if total_claims_count == 0:
            return 0.0
        return verified_claims_count / total_claims_count

    def score_report(self, benchmark: Dict[str, Any], actual_data: Dict[str, Any]) -> EvalResult:
        # Simplified scoring logic for assignment
        coverage = self.calculate_coverage(
            actual_data.get("claims", []),
            benchmark.get("expected_claims", [])
        )

        return EvalResult(
            benchmark_id=benchmark["id"],
            grounding_score=actual_data.get("grounding", 0.8),
            coverage_score=coverage,
            citation_validity=actual_data.get("citation_validity", 0.9),
            consistency_score=actual_data.get("consistency", 0.85)
        )
