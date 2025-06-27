import os
import json
import logging
from typing import List, Dict

import redis.asyncio as aioredis
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL")

_redis = None
_memory_store: Dict[str, List[Dict[str, str]]] = {}

if REDIS_URL:
    try:
        _redis = aioredis.from_url(REDIS_URL, decode_responses=True)
        logger.info("Connected to Redis at %s", REDIS_URL)
    except Exception as exc:
        logger.warning("Redis connection failed: %s", exc)
        _redis = None


async def get_session(key: str) -> List[Dict[str, str]]:
    """Retrieve a chat session list from Redis or in-memory store."""
    if _redis:
        data = await _redis.get(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                logger.warning("Invalid session data for %s", key)
    return _memory_store.get(key, [])


async def save_session(key: str, session: List[Dict[str, str]]) -> None:
    """Persist chat session to Redis and memory."""
    if _redis:
        await _redis.set(key, json.dumps(session))
    _memory_store[key] = session
