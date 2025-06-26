"""Razorpay integration for payment links."""

import os
from typing import Dict

import razorpay

CLIENT = razorpay.Client(
    auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
)

def create_payment_link(amount: int, description: str) -> str:
    """Return a short payment URL from Razorpay."""
    data = {
        "amount": amount * 100,  # Razorpay accepts paise
        "currency": "INR",
        "description": description,
    }
    link = CLIENT.payment_link.create(data)
    return link.get("short_url")


def verify_signature(body: bytes, signature: str) -> bool:
    try:
        razorpay.Utility.verify_webhook_signature(
            body, signature, os.getenv("RAZORPAY_WEBHOOK_SECRET")
        )
        return True
    except razorpay.errors.SignatureVerificationError:
        return False

