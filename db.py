"""MongoDB integration using Motor."""

import os
from typing import Any, Dict
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_default_database()

async def save_user(user: Dict[str, Any]) -> str:
    res = await db.users.insert_one(user)
    return str(res.inserted_id)

async def save_chat(chat: Dict[str, Any]) -> str:
    res = await db.chats.insert_one(chat)
    return str(res.inserted_id)

async def save_summary(summary: Dict[str, Any]) -> str:
    res = await db.summaries.insert_one(summary)
    return str(res.inserted_id)

async def get_user_by_phone(phone: str) -> Dict[str, Any] | None:
    return await db.users.find_one({"phone": phone})

