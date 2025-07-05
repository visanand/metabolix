"""FastAPI entrypoint for the Metabolix chatbot."""

import logging
import os
import asyncio
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes import router

from db import db
from nudge import start_nudge_loop

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI(title=os.getenv("BOT_NAME", "MetabolixBot"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check() -> dict[str, str]:
    """Simple health check."""
    logger.debug("Health check called")
    return {"status": "ok"}

app.include_router(router)


@app.on_event("startup")
async def start_tasks() -> None:
    """Launch background tasks on startup."""
    asyncio.create_task(start_nudge_loop())


if __name__ == "__main__":
    import uvicorn

    port: int = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

