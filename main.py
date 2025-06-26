from typing import Optional
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

if __name__ == "__main__":
    import uvicorn

    port: int = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

"""FastAPI entrypoint for AarogyaAI."""

import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

=======
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes import router

>>>>>>> main
load_dotenv()
app = FastAPI(title=os.getenv("BOT_NAME", "AarogyaAI"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< e5mhwf-codex/build-multilingual-healthcare-assistant--aarogyaai

@app.get("/")
async def health_check() -> dict[str, str]:
    """Simple health check."""
    logger.debug("Health check called")
    return {"status": "ok"}

=======
>>>>>>> main
app.include_router(router)

