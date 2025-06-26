"""OpenAI GPT-4 integration for AarogyaAI."""

import logging
import os
from typing import Dict, List

from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are AarogyaAI, an assistive health chatbot. "
    "Provide general health education and symptom triage. "
    "Never prescribe medication. Escalate to an RMP when red flags appear."
)

async def generate_response(messages: List[Dict[str, str]]) -> str:
    """Call OpenAI's API and return the assistant's reply."""
    chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    try:
        resp = await client.chat.completions.create(
            model="gpt-4",
            messages=chat_messages,
            temperature=0.6,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        logger.exception("OpenAI request failed: %s", exc)
        return "Sorry, I couldn't process that right now."

