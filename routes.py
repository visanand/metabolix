"""FastAPI route handlers for AarogyaAI."""

import logging
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import Response

from chat_engine import generate_response, PAYMENT_PLACEHOLDER
from db import save_user, save_chat, save_summary
from schemas import (
    Consent,
    UserInfo,
    SymptomData,
    Summary,
    StartPayload,
    ConsultRequest,
)
from utils import timestamp
from razorpay_utils import create_payment_link, verify_signature
from db import db
from session_store import get_session, save_session
from twilio.twiml.messaging_response import MessagingResponse

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


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    sender = form["From"].split(":")[-1]  # Extract phone
    message = form["Body"].strip()

    session = await get_session(sender)
    session.append({"role": "user", "content": message})

    try:
        reply = await generate_response(session)

        if PAYMENT_PLACEHOLDER in reply:
            link = await create_payment_link(99, "AarogyaAI consult")
            reply = reply.replace(PAYMENT_PLACEHOLDER, link)
        session.append({"role": "assistant", "content": reply})
    except Exception:
        reply = "Sorry, something went wrong. Please try again."
        session.append({"role": "assistant", "content": reply})

    await save_session(sender, session)
    await save_chat({"phone": sender, "input": message, "output": reply})

    resp = MessagingResponse()
    resp.message(reply)
    return Response(content=str(resp), media_type="application/xml")


@router.post("/summary")
async def store_summary(summary: Summary):
    logger.info("Storing summary for %s", summary.user_phone)
    await save_summary(summary.dict())
    return {"status": "saved"}


@router.post("/payment-webhook")
async def payment_webhook(request: Request):
    signature = request.headers.get("X-Razorpay-Signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing Razorpay signature")

    body = await request.body()

    if not verify_signature(body, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    payload = await request.json()
    event = payload.get("event")
    entity = payload.get("payload", {}).get("payment", {}).get("entity")

    if not event or not entity:
        raise HTTPException(status_code=400, detail="Invalid Razorpay payload")

    await save_chat({
        "event": event,
        "entity": entity,
        "raw_payload": payload,
        "time": timestamp()
    })

    return {"status": "ok"}


