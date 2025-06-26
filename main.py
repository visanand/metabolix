from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< yw4l2s-codex/build-multilingual-healthcare-assistant--aarogyaai
from dotenv import load_dotenv
import os

from routes import router

load_dotenv()
app = FastAPI(title=os.getenv("BOT_NAME", "AarogyaAI"))
=======

from routes import router

app = FastAPI(title="AarogyaAI")
>>>>>>> main

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

