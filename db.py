"""Async MongoDB integration using Motor with TLS and certifi."""

import os
import logging
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import certifi

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI")

# Async client and DB handle
client: Optional[AsyncIOMotorClient] = None
db = None

# Setup MongoDB connection with TLS
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
        logger.info("Connected to MongoDB successfully.")
    except Exception as e:
        logger.error(f"MongoDB connection error: {e}")
else:
    logger.warning("MONGODB_URI not set. Database not configured.")

# === Async DB Operations ===

async def save_user(user: Dict[str, Any]) -> str:
    """Create or update a user profile."""
    if db is None:
        raise RuntimeError("Database not configured")
    phone = user.get("phone")
    if not phone:
        res = await db.users.insert_one(user)
        logger.info("Saved user with id %s", res.inserted_id)
        return str(res.inserted_id)

    await db.users.update_one(
        {"phone": phone},
        {
            "$set": user,
            "$setOnInsert": {"chats": [], "payments": []},
        },
        upsert=True,
    )
    doc = await db.users.find_one({"phone": phone}, {"_id": 1})
    logger.info("Saved user with phone %s", phone)
    return str(doc["_id"])

async def save_chat(chat: Dict[str, Any]) -> str:
    if db is None:
        raise RuntimeError("Database not configured")
    res = await db.chats.insert_one(chat)
    logger.debug("Saved chat with id %s", res.inserted_id)
    return str(res.inserted_id)


async def append_chat(phone: str, user_text: str, bot_text: str, time: str) -> None:
    """Append a chat message to the user's conversation history."""
    if db is None:
        raise RuntimeError("Database not configured")
    await db.users.update_one(
        {"phone": phone},
        {
            "$push": {
                "chats": {"input": user_text, "output": bot_text, "time": time}
            }
        },
        upsert=True,
    )

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


async def update_user_language(phone: str, language: str) -> None:
    """Store the last used language for a user."""
    if db is None:
        raise RuntimeError("Database not configured")
    await db.users.update_one({"phone": phone}, {"$set": {"language": language}})
    logger.debug("Updated language for %s to %s", phone, language)


async def record_payment(phone: str, payment: Dict[str, Any]) -> None:
    """Store a payment event for a user."""
    if db is None:
        raise RuntimeError("Database not configured")
    await db.users.update_one(
        {"phone": phone},
        {"$push": {"payments": payment}},
        upsert=True,
    )
    

async def mark_payment_paid(phone: str, link_id: str, payment_id: str) -> None:
    """Update a pending payment's status to paid."""
    if db is None:
        raise RuntimeError("Database not configured")
    await db.users.update_one(
        {"phone": phone, "payments.link_id": link_id},
        {"$set": {"payments.$.status": "paid", "payments.$.payment_id": payment_id}},
    )
