"""FastAPI route handlers for AarogyaAI."""

import logging
import asyncio
from typing import Optional
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import Response

from chat_engine import generate_response, PAYMENT_PLACEHOLDER
from db import (
    save_user,
    save_chat,
    save_summary,
    get_user_by_phone,
    update_user_language,
    append_chat,
    record_payment,
    mark_payment_paid,
)
from schemas import (
    Consent,
    UserInfo,
    SymptomData,
    Summary,
    StartPayload,
    ConsultRequest,
)
from utils import timestamp, detect_language, send_whatsapp_message
from razorpay_utils import (
    create_payment_link,
    verify_signature,
    is_payment_complete,
)
from session_store import get_session, save_session
from twilio.twiml.messaging_response import MessagingResponse

logger = logging.getLogger(__name__)

router = APIRouter()


async def confirm_pending_payment(phone: str) -> Optional[str]:
    """Check if user has a pending payment that is now paid."""
    user = await get_user_by_phone(phone)
    if not user:
        return None
    payments = user.get("payments", [])
    for p in reversed(payments):
        if p.get("status") == "pending" and p.get("link_id"):
            info = await is_payment_complete(p["link_id"])
            if info:
                await mark_payment_paid(phone, p["link_id"], info["payment_id"])
                await record_payment(
                    phone,
                    {
                        "payment_id": info["payment_id"],
                        "amount": info["amount"],
                        "status": "paid",
                        "time": timestamp(),
                    },
                )
                msg = (
                    f"Payment confirmed. Transaction ID: {info['payment_id']}. "
                    "A doctor will reach you within 24 hours."
                )
                return msg
    return None


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
    link = await create_payment_link(amount, f"AarogyaAI {consult_type} consult", payload.user.phone)
    await save_chat({
        "user": payload.user.dict(),
        "symptoms": payload.symptoms.dict(),
        "consult_type": consult_type,
        "requested_at": timestamp(),
        "payment_link": link["url"],
    })
    await record_payment(
        payload.user.phone,
        {
            "amount": amount,
            "link": link["url"],
            "link_id": link["id"],
            "status": "pending",
            "time": timestamp(),
        },
    )
    return {"payment_link": link["url"]}


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    print("Webhook Triggered")
    try:
        form = await request.form()
        sender = form["From"].split(":")[-1]  # Extract phone
        message = form["Body"].strip()
        num_media = int(form.get("NumMedia", 0))

        language = detect_language(message)
        try:
            await update_user_language(sender, language)
        except RuntimeError:
            pass

        session = await get_session(sender)
        if not session:
            user = await get_user_by_phone(sender)
            if user:
                meta = (
                    f"Returning user details: name={user.get('name')}, "
                    f"age={user.get('age')}, gender={user.get('gender')}, "
                    f"pin={user.get('pin')}"
                )
                session.append({"role": "system", "content": meta})

        session.append({"role": "user", "content": message or "<media>"})

        confirmation = await confirm_pending_payment(sender)

        if num_media > 0 and confirmation:
            session.append({"role": "assistant", "content": confirmation})
            await save_session(sender, session)
            await append_chat(sender, "<media>", confirmation, timestamp())
            await save_chat({"phone": sender, "input": "<media>", "output": confirmation})
            resp = MessagingResponse()
            resp.message(confirmation)
            return Response(content=str(resp), media_type="application/xml")

        # Ensure OpenAI call is time-limited
        try:
            reply = await asyncio.wait_for(generate_response(session, language), timeout=12)

            if PAYMENT_PLACEHOLDER in reply:
                link = await create_payment_link(99, "AarogyaAI consult", sender)
                reply = reply.replace(PAYMENT_PLACEHOLDER, link["url"])
                await record_payment(
                    sender,
                    {
                        "amount": 99,
                        "link": link["url"],
                        "link_id": link["id"],
                        "status": "pending",
                        "time": timestamp(),
                    },
                )
            if confirmation:
                reply = f"{confirmation}\n\n{reply}"

        except asyncio.TimeoutError:
            reply = "Sorry, the system is currently slow. Please try again in a few minutes."
        except Exception as e:
            print(f"❌ Error generating reply: {e}")
            reply = "Sorry, something went wrong. Please try again."

        session.append({"role": "assistant", "content": reply})
        await save_session(sender, session)
        await append_chat(sender, message, reply, timestamp())
        await save_chat({"phone": sender, "input": message, "output": reply})

        resp = MessagingResponse()
        resp.message(reply)
        return Response(content=str(resp), media_type="application/xml")

    except Exception as e:
        print(f"❌ Top-level webhook error: {e}")
        fallback = MessagingResponse()
        fallback.message("Sorry, something went wrong on our side. We'll fix it soon.")
        return Response(content=str(fallback), media_type="application/xml")

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

    contact = entity.get("contact")
    if contact:
        await record_payment(
            contact,
            {
                "payment_id": entity.get("id"),
                "amount": entity.get("amount", 0) / 100,
                "status": entity.get("status"),
                "time": timestamp(),
            },
        )
        await send_whatsapp_message(
            contact,
            f"Payment confirmed. Transaction ID: {entity.get('id')}. A doctor will reach you within 24 hours.",
        )


    return {"status": "ok"}


