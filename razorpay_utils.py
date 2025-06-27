"""Razorpay integration for payment links."""

import logging
import os
from typing import Dict
from dotenv import load_dotenv

import razorpay
import asyncio

load_dotenv()
CLIENT = razorpay.Client(
    auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
)
logger = logging.getLogger(__name__)

async def create_payment_link(amount: int, description: str) -> str:
    data = {
        "amount": amount * 100,  # Razorpay accepts paise
        "currency": "INR",
        "description": description,
    }
    logger.info("Creating payment link for amount %s", amount)
    link = await asyncio.to_thread(CLIENT.payment_link.create, data)
    url = link.get("short_url")
    logger.info("Payment link created: %s", url)
    return url


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

