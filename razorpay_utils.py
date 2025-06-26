"""Razorpay integration for payment links."""

import os
from typing import Dict
<<<<<<< yw4l2s-codex/build-multilingual-healthcare-assistant--aarogyaai
from dotenv import load_dotenv

import razorpay

load_dotenv()
=======

import razorpay

>>>>>>> main
CLIENT = razorpay.Client(
    auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
)

<<<<<<< yw4l2s-codex/build-multilingual-healthcare-assistant--aarogyaai
async def create_payment_link(amount: int, description: str) -> str:
=======
def create_payment_link(amount: int, description: str) -> str:
    """Return a short payment URL from Razorpay."""
>>>>>>> main
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

