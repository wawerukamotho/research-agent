import json
from typing import Any, Dict, Optional
from uuid import UUID
import redis.asyncio as redis
from context.models import Checkpoint, ResearchSession
from scaffold.config import settings
from scaffold.logging import logger

class CheckpointManager:
    def __init__(self, redis_client: redis.Redis = None):
        self._redis = redis_client or redis.from_url(settings.redis_url)

    async def save_checkpoint(self, session_id: UUID, checkpoint: Checkpoint):
        key = f"checkpoint:{session_id}"
        await self._redis.rpush(key, checkpoint.model_dump_json())
        logger.info("checkpoint_saved", session_id=str(session_id), checkpoint_id=str(checkpoint.id))

    async def get_latest_checkpoint(self, session_id: UUID) -> Optional[Checkpoint]:
        key = f"checkpoint:{session_id}"
        data = await self._redis.lindex(key, -1)
        if data:
            return Checkpoint.model_validate_json(data)
        return None

    async def save_session(self, session: ResearchSession):
        key = f"session:{session.id}"
        await self._redis.set(key, session.model_dump_json())
        logger.info("session_saved", session_id=str(session.id))

    async def get_session(self, session_id: UUID) -> Optional[ResearchSession]:
        key = f"session:{session_id}"
        data = await self._redis.get(key)
        if data:
            return ResearchSession.model_validate_json(data)
        return None
