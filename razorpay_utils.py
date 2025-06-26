"""Razorpay integration for payment links."""

import os
from typing import Dict
from dotenv import load_dotenv

import razorpay
import asyncio

load_dotenv()
CLIENT = razorpay.Client(
    auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
)

async def create_payment_link(amount: int, description: str) -> str:
    data = {
        "amount": amount * 100,  # Razorpay accepts paise
        "currency": "INR",
        "description": description,
    }
    link = await asyncio.to_thread(CLIENT.payment_link.create, data)
    return link.get("short_url")


def verify_signature(body: bytes, signature: str) -> bool:
    try:
        razorpay.Utility.verify_webhook_signature(
            body, signature, os.getenv("RAZORPAY_WEBHOOK_SECRET")
        )
        return True
    except razorpay.errors.SignatureVerificationError:
        return False