"""OpenAI GPT-4 integration for AarogyaAI."""

import os
from typing import List, Dict

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You are AarogyaAI, an assistive health chatbot. "
    "Provide general health education and symptom triage. "
    "Never prescribe medication. Escalate to an RMP when red flags appear."
)

async def generate_response(messages: List[Dict[str, str]]) -> str:
    """Call OpenAI's API and return the assistant's reply."""
    if not openai.api_key:
        return "AI service unavailable."

    chat_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    try:
        resp = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=chat_messages,
            temperature=0.6,
        )
        return resp.choices[0].message["content"].strip()
    except Exception:
        return "Sorry, I couldn't process that right now."

