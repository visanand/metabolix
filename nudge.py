import asyncio
import logging
import os
from datetime import datetime, timedelta

from db import db
from utils import send_whatsapp_message

logger = logging.getLogger(__name__)

NUDGE_HOURS = int(os.getenv("NUDGE_HOURS", "20"))
NUDGE_TEXT = os.getenv(
    "NUDGE_TEXT",
    "Hi! We noticed you haven't continued our chat. Complete your order today and get 5% off!",
)


async def check_and_nudge() -> None:
    """Send a nudge message to inactive users."""
    if db is None:
        logger.debug("Database not configured; skipping nudge check")
        return

    cutoff = datetime.utcnow() - timedelta(hours=NUDGE_HOURS)
    async for user in db.users.find({"chats": {"$ne": []}}):
        last_chat = user.get("chats", [])[-1]
        if not last_chat:
            continue
        try:
            last_time = datetime.fromisoformat(last_chat.get("time"))
        except Exception:
            continue
        last_nudge_time = user.get("last_nudge")
        if last_nudge_time:
            try:
                last_nudge = datetime.fromisoformat(last_nudge_time)
            except Exception:
                last_nudge = None
        else:
            last_nudge = None
        if last_time < cutoff and (not last_nudge or last_nudge < last_time):
            phone = user.get("phone")
            if phone:
                name = user.get("name", "there")
                text = f"Hi {name}! {NUDGE_TEXT}"
                await send_whatsapp_message(phone, text)
                await db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"last_nudge": datetime.utcnow().isoformat()}},
                )
                logger.info("Sent nudge to %s", phone)


async def start_nudge_loop() -> None:
    """Background loop to periodically nudge inactive users."""
    while True:
        try:
            await check_and_nudge()
        except Exception as exc:
            logger.exception("Nudge check failed: %s", exc)
        await asyncio.sleep(3600)

