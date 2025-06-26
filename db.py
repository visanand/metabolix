"""MongoDB integration using Motor with TLS and Certifi CA support."""

import logging
import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import certifi

from motor.motor_asyncio import AsyncIOMotorClient

# Load .env
load_dotenv()

# Logger setup
logger = logging.getLogger(__name__)

# MongoDB URI from environment
MONGODB_URI = os.getenv("MONGODB_URI")

# Initialize client
client: Optional[AsyncIOMotorClient] = None
db = None

if MONGODB_URI:
    try:
        client = AsyncIOMotorClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=10000,
            tls=True,
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=os.getenv("MONGODB_ALLOW_INVALID_CERTS", "false").lower() == "true"
        )
        db = client.get_default_database()
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        client = None
        db = None
else:
    logger.warning("MONGODB_URI not set in environment")

# === Database Operations ===

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

async def get_user_by_phone(phone: str) -> Optional[Dict[str, Any]]:
    if db is None:
        raise RuntimeError("Database not configured")
    user = await db.users.find_one({"phone": phone})
    logger.debug("Fetched user by phone %s: %s", phone, bool(user))
    return user
