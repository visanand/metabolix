"""API endpoints for AarogyaAI."""

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.concurrency import run_in_threadpool

from chat_engine import generate_response
from db import save_user, save_chat, save_summary
from schemas import (
    StartPayload,
    UserInfo,
    SymptomData,
    Summary,
    PaymentWebhook,
)
from utils import timestamp
from razorpay_utils import create_payment_link, verify_signature

router = APIRouter()


@router.post("/start")
async def start_chat(payload: StartPayload):
    consent = payload.consent
    user = payload.user
    if not consent.accepted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Consent required"
        )
    user_dict = user.dict()
    user_dict["consent_time"] = consent.timestamp
    await save_user(user_dict)
    return {"message": f"Welcome {user.name}! How can I help you today?"}


@router.post("/triage")
async def triage(symptom: SymptomData):
    messages = [{"role": "user", "content": symptom.description}]
    reply = await generate_response(messages)
    await save_chat({"input": symptom.description, "output": reply, "time": timestamp()})
    return {"reply": reply}


@router.post("/consult")
async def consult(request: UserInfo):
    link = await run_in_threadpool(create_payment_link, 99, "AarogyaAI Consult")
    return {"payment_link": link}


@router.post("/summary")
async def store_summary(summary: Summary):
    await save_summary(summary.dict())
    return {"status": "saved"}


@router.post("/payment-webhook")
async def payment_webhook(request: Request):
    signature = request.headers.get("X-Razorpay-Signature")
    body = await request.body()
    if not verify_signature(body, signature or ""):
        raise HTTPException(status_code=400, detail="Invalid signature")
    payload = await request.json()
    await save_chat({"payment_event": payload, "time": timestamp()})
    return {"status": "ok"}

