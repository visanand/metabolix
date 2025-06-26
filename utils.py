"""Utility helpers for AarogyaAI."""

import re
from datetime import datetime

AGE_PATTERN = re.compile(r"^\d{1,3}$")
PIN_PATTERN = re.compile(r"^\d{6}$")


def validate_age(age: str) -> bool:
    return AGE_PATTERN.match(age) is not None and 0 < int(age) <= 120


def validate_pin(pin: str) -> bool:
    return PIN_PATTERN.match(pin) is not None


def timestamp() -> str:
    return datetime.utcnow().isoformat()

