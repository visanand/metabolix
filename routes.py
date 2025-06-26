"""FastAPI route handlers for AarogyaAI."""

import logging
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import PlainTextResponse

from chat_engine import generate_response
from db import save_user, save_chat, save_summary
from schemas import (
    Consent,
    UserInfo,
    SymptomData,
    Summary,
    PaymentWebhook,
    StartPayload,
    ConsultRequest,
)
from utils import timestamp
from razorpay_utils import create_payment_link, verify_signature

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/start")
async def start_chat(payload: StartPayload):
    logger.info("Starting chat for %s", payload.user.phone or payload.user.name)
    if not payload.consent.accepted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Consent required")
    user_dict = payload.user.dict()
    user_dict["consent_time"] = payload.consent.timestamp
    await save_user(user_dict)
    return {"message": f"Welcome {payload.user.name}! How can I help you today?"}


@router.post("/triage")
async def triage(symptom: SymptomData):
    logger.debug("Triage request: %s", symptom.description)
    messages = [{"role": "user", "content": symptom.description}]
    reply = await generate_response(messages)
    await save_chat({"input": symptom.description, "output": reply, "time": timestamp()})
    return {"reply": reply}


@router.post("/consult")
async def consult(payload: ConsultRequest, consult_type: str = "audio"):
    logger.info("Consult requested type=%s", consult_type)
    amount = 99 if consult_type == "audio" else 249
    link = await create_payment_link(amount, f"AarogyaAI {consult_type} consult")
    await save_chat({
        "user": payload.user.dict(),
        "symptoms": payload.symptoms.dict(),
        "consult_type": consult_type,
        "requested_at": timestamp(),
        "payment_link": link,
    })
    return {"payment_link": link}


@router.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_webhook(request: Request) -> str:
    """Minimal Twilio-style WhatsApp webhook handler."""
    form = await request.form()
    message = form.get("Body", "")
    logger.debug("WhatsApp message received: %s", message)
    reply = await generate_response([{"role": "user", "content": message}])
    await save_chat({"input": message, "output": reply, "time": timestamp()})
    return f"<Response><Message>{reply}</Message></Response>"


@router.post("/summary")
async def store_summary(summary: Summary):
    logger.info("Storing summary for %s", summary.user_phone)
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

