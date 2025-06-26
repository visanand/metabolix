"""OpenAI GPT-4 integration for AarogyaAI."""

<<<<<<< e5mhwf-codex/build-multilingual-healthcare-assistant--aarogyaai
import logging
import os
from typing import Dict, List

from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)
=======
import os
from typing import List, Dict

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
>>>>>>> main

SYSTEM_PROMPT = (
    "You are AarogyaAI, an assistive health chatbot. "
    "Provide general health education and symptom triage. "
    "Never prescribe medication. Escalate to an RMP when red flags appear."
)

async def generate_response(messages: List[Dict[str, str]]) -> str:
    """Call OpenAI's API and return the assistant's reply."""
<<<<<<< e5mhwf-codex/build-multilingual-healthcare-assistant--aarogyaai
    chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    try:
        resp = await client.chat.completions.create(
=======
    if not openai.api_key:
        return "AI service unavailable."

    chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    try:
        resp = await openai.ChatCompletion.acreate(
>>>>>>> main
            model="gpt-4",
            messages=chat_messages,
            temperature=0.6,
        )
<<<<<<< e5mhwf-codex/build-multilingual-healthcare-assistant--aarogyaai
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        logger.exception("OpenAI request failed: %s", exc)
=======
        return resp.choices[0].message["content"].strip()
    except Exception:
>>>>>>> main
        return "Sorry, I couldn't process that right now."

