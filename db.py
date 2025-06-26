"""MongoDB integration using Motor."""

import logging
import os
from typing import Any, Dict
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
logger = logging.getLogger(__name__)

client = AsyncIOMotorClient(MONGODB_URI) if MONGODB_URI else None
db = client.get_default_database() if client else None

async def save_user(user: Dict[str, Any]) -> str:
    if db is None:
        raise RuntimeError("Database not configured")
    res = await db.users.insert_one(user)
    logger.info("Saved user with id %s", res.inserted_id)
    return str(res.inserted_id)

async def save_chat(chat: Dict[str, Any]) -> str:
    if db is None:
        raise RuntimeError("Database not configured")
    res = await db.chats.insert_one(chat)
    logger.debug("Saved chat with id %s", res.inserted_id)
    return str(res.inserted_id)

async def save_summary(summary: Dict[str, Any]) -> str:
    if db is None:
        raise RuntimeError("Database not configured")
    res = await db.summaries.insert_one(summary)
    logger.info("Saved summary with id %s", res.inserted_id)
    return str(res.inserted_id)

async def get_user_by_phone(phone: str) -> Dict[str, Any] | None:
    if db is None:
        raise RuntimeError("Database not configured")
    user = await db.users.find_one({"phone": phone})
    logger.debug("Fetched user by phone %s: %s", phone, bool(user))
    return user

