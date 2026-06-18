from typing import List
import litellm
from scaffold.config import settings
from scaffold.logging import logger

class RollingSummaryManager:
    def __init__(self, model: str = None, max_summary_tokens: int = 500):
        self.model = model or settings.default_llm_model
        self.max_tokens = max_summary_tokens
        self.summary = ""

    async def update_summary(self, new_info: str):
        prompt = f"""
        Current Research Summary:
        {self.summary}

        New Information to Integrate:
        {new_info}

        Task: Update the research summary with the new information.
        Keep it concise (under {self.max_tokens} tokens).
        Maintain key findings and citations.
        """

        try:
            response = await litellm.acompletion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            self.summary = response.choices[0].message.content
            logger.info("summary_updated", summary_length=len(self.summary))
        except Exception as e:
            logger.error("summary_update_failed", error=str(e))
            # Graceful degradation: append if model fails
            self.summary = (self.summary + "\n" + new_info)[:self.max_tokens * 4]

    def get_summary(self) -> str:
        return self.summary
