"""Utility helpers for the Metabolix chatbot."""

import re
from datetime import datetime
from typing import Optional
import os
import asyncio
import logging

from twilio.rest import Client

from langdetect import detect, DetectorFactory, LangDetectException

AGE_PATTERN = re.compile(r"^\d{1,3}$")
PIN_PATTERN = re.compile(r"^\d{6}$")


def validate_age(age: str) -> bool:
    return AGE_PATTERN.match(age) is not None and 0 < int(age) <= 120


def validate_pin(pin: str) -> bool:
    return PIN_PATTERN.match(pin) is not None


DetectorFactory.seed = 0

LANG_MAP = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "pa": "Punjabi",
}


def detect_language(text: str) -> str:
    """Detect language of user text and return readable name."""
    try:
        code = detect(text)
        return LANG_MAP.get(code, "English")
    except LangDetectException:
        return "English"


def timestamp() -> str:
    return datetime.utcnow().isoformat()


# --- Twilio helper functions ---
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

_twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    try:
        _twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    except Exception as exc:
        logging.warning("Twilio client init failed: %s", exc)
        _twilio_client = None


async def send_whatsapp_message(phone: str, text: str) -> None:
    """Send a WhatsApp message via Twilio if configured."""
    if not _twilio_client or not TWILIO_WHATSAPP_NUMBER:
        return
    await asyncio.to_thread(
        _twilio_client.messages.create,
        body=text,
        from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
        to=f"whatsapp:{phone}",
    )

# --- Admin notification helper ---
ADMIN_PHONE = os.getenv("ADMIN_PHONE", "+919810519452")


async def notify_admin(text: str) -> None:
    """Send a WhatsApp message to the admin number."""
    await send_whatsapp_message(ADMIN_PHONE, text)

