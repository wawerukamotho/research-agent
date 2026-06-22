import json
from typing import Any, Dict, List
from scaffold.llm import safe_acompletion
from tools.analyze.base import AnalysisProvider
from scaffold.config import settings
from scaffold.logging import logger

class LLMAnalysisProvider(AnalysisProvider):
    def __init__(self, model: str = None):
        self.model = model or settings.default_llm_model

    async def analyze(self, text: str, task: str, schema: Any, context: str = None) -> Any:
        # For Phase 10, handle potential None text by using context if documents/claims provided
        if text is None:
            text = "Data provided in structured format (documents/claims)."

        prompt = f"""
        Task: {task}

        Text to analyze:
        {text}

        Additional Context:
        {context or 'No additional context provided.'}

        Return the result strictly as JSON matching this schema:
        {json.dumps(schema.model_json_schema() if hasattr(schema, 'model_json_schema') else schema)}
        """

        try:
            response = await safe_acompletion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            data = json.loads(content)

            if hasattr(schema, "model_validate"):
                return schema.model_validate(data)
            return data
        except Exception as e:
            logger.error("llm_analysis_failed", error=str(e), task=task)
            # For Phase 5, if LLM fails or no keys, we can return a mock or raise
            raise
