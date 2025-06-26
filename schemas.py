"""Pydantic models for AarogyaAI."""

from typing import List, Optional
from pydantic import BaseModel, Field


class Consent(BaseModel):
    accepted: bool
    timestamp: str


class UserInfo(BaseModel):
    name: str
    age: int
    gender: str
    location: str
    phone: Optional[str] = None


class SymptomData(BaseModel):
    description: str
    duration: Optional[str] = None
    severity: Optional[str] = None


class ConsultRequest(BaseModel):
    user: UserInfo
    symptoms: SymptomData


class StartPayload(BaseModel):
    """Payload for chat start containing consent and user info."""
    consent: Consent
    user: UserInfo


class Summary(BaseModel):
    user_phone: Optional[str]
    summary: str
    consult_id: Optional[str] = None


class PaymentWebhook(BaseModel):
    payload: dict

