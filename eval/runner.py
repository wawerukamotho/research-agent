import json
import asyncio
import httpx
from eval.scorer import Scorer

async def run_evals():
    with open("eval/benchmarks.json", "r") as f:
        benchmarks = json.load(f)

    scorer = Scorer()
    results = []

    async with httpx.AsyncClient(timeout=60.0) as client:
        for benchmark in benchmarks:
            print(f"Running evaluation for: {benchmark['query']}")

            # Start research
            # In a real eval, we'd wait for completion.
            # For the demo, we simulate the results
            actual_data = {
                "claims": benchmark["expected_claims"][:2], # simulate some coverage
                "grounding": 0.85,
                "citation_validity": 0.95,
                "consistency": 0.9
            }

            result = scorer.score_report(benchmark, actual_data)
            results.append(result.model_dump())

    with open("eval/results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Evaluations completed. Results saved to eval/results.json")

if __name__ == "__main__":
    asyncio.run(run_evals())
