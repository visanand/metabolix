"""Razorpay integration for payment links."""

import logging
import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv

import razorpay
import asyncio

load_dotenv()
CLIENT = razorpay.Client(
    auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
)
logger = logging.getLogger(__name__)

async def create_payment_link(amount: int, description: str, phone: str) -> Dict[str, str]:
    """Create a payment link and return its id and short URL."""
    data = {
        "amount": amount * 100,  # Razorpay accepts paise
        "currency": "INR",
        "description": description,
        "customer": {"contact": phone},
    }
    logger.info("Creating payment link for amount %s to %s", amount, phone)
    link = await asyncio.to_thread(CLIENT.payment_link.create, data)
    result = {"id": link.get("id"), "url": link.get("short_url")}
    logger.info("Payment link created: %s", result["url"])
    return result


async def fetch_payment_link(link_id: str) -> Dict[str, Any]:
    """Fetch payment link details from Razorpay."""
    return await asyncio.to_thread(CLIENT.payment_link.fetch, link_id)


async def is_payment_complete(link_id: str) -> Optional[Dict[str, Any]]:
    """Check if a payment link is paid and return info if so."""
    data = await fetch_payment_link(link_id)
    if data.get("status") == "paid":
        return {
            "payment_id": data.get("payment_id"),
            "amount": data.get("amount", 0) / 100,
        }
    return None


def verify_signature(body: bytes, signature: str) -> bool:
    try:
        CLIENT.utility.verify_webhook_signature(
            body, signature, os.getenv("RAZORPAY_WEBHOOK_SECRET")
        )
        logger.debug("Payment webhook signature valid")
        return True
    except razorpay.errors.SignatureVerificationError:
        logger.warning("Invalid payment webhook signature")
        return False

