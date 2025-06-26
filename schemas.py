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


class StartPayload(BaseModel):
    """Payload for the `/start` route combining consent and user info."""

    consent: Consent
    user: UserInfo


class SymptomData(BaseModel):
    description: str
    duration: Optional[str] = None
    severity: Optional[str] = None


class ConsultRequest(BaseModel):
    user: UserInfo
    symptoms: SymptomData


class Summary(BaseModel):
    user_phone: Optional[str]
    summary: str
    consult_id: Optional[str] = None




