"""OpenAI GPT-4 integration for the Metabolix chatbot."""

import logging
import os
from typing import Dict, List

from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger = logging.getLogger(__name__)

PAYMENT_PLACEHOLDER = "<PAYMENT_LINK>"

SYSTEM_PROMPT_TEMPLATE = f"""
You are Metabolix, a WhatsApp chatbot that helps users learn about weight-loss products and medical weight management services from mymetabolix.com.
Your tasks are:
1. Greet the user and confirm their consent to chat.
2. Collect basic details like name, age, gender and city if consent is given.
3. Answer questions about Metabolix products and medical weight loss.
4. Offer to book an appointment or take a product order when the user requests.
   Provide a short confirmation message containing the token {PAYMENT_PLACEHOLDER} if a paid consult is needed.
5. Keep responses short and clear for WhatsApp in {{language}}.

Always remind users that this is not medical advice and they should consult a doctor for any concerns.
"""

async def generate_response(messages: List[Dict[str, str]], language: str = "English") -> str:
    """Call OpenAI's API and return the assistant's reply."""
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(language=language)
    chat_messages = [{"role": "system", "content": system_prompt}] + messages
    try:
        resp = await client.chat.completions.create(
            model="gpt-4",
            messages=chat_messages,
            temperature=0.6,
            timeout=10,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        logger.exception("OpenAI request failed: %s", exc)
        return "Sorry, I couldn't process that right now. Please try after some time."

