import logging
from fastapi.middleware.cors import CORSMiddleware

from backend import app
from backend.api.email import router as email_router
from backend.api.chatbot import router as chatbot_router
from backend.configs.log import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_router)
app.include_router(chatbot_router)


@app.get("/")
def read_root():
    return {
        "info": "IT-Meet-2025 Backend",
        "status": "running",
    }
