import json
from typing import Any
import litellm
from tools.write.base import WriteProvider
from scaffold.config import settings
from scaffold.logging import logger

class LLMWriteProvider(WriteProvider):
    def __init__(self, model: str = None):
        self.model = model or settings.default_llm_model

    async def generate(self, prompt: str, task: str, schema: Any, context: str = None) -> Any:
        full_prompt = f"""
        Task: {task}

        Prompt:
        {prompt}

        Context:
        {context or 'No additional context provided.'}

        Return the result strictly as JSON matching this schema:
        {json.dumps(schema.model_json_schema() if hasattr(schema, 'model_json_schema') else schema)}
        """

        try:
            response = await litellm.acompletion(
                model=self.model,
                messages=[{"role": "user", "content": full_prompt}],
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            data = json.loads(content)

            if hasattr(schema, "model_validate"):
                return schema.model_validate(data)
            return data
        except Exception as e:
            logger.error("llm_write_failed", error=str(e), task=task)
            raise
