import logging
from fastapi import HTTPException
import httpx
from fastapi import APIRouter
from pydantic import BaseModel
from pydantic import EmailStr

from backend.configs.environment import GOOGLE_SCRIPT_URL

router = APIRouter()
logger = logging.getLogger(__name__)


class EmailRequest(BaseModel):
    email: EmailStr


@router.post("/submit-email")
async def submit_email(data: EmailRequest):
    if not GOOGLE_SCRIPT_URL:
        logger.error("GOOGLE_SCRIPT_URL missing")
        raise HTTPException(500, "Server misconfigured. Missing an environment key")

    payload = {"email": data.email}
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(GOOGLE_SCRIPT_URL, json=payload)
    except Exception as e:
        logger.exception(f"Failed to send email to script. Error: {e}")
        raise HTTPException(500, "Failed to connect with google script")

    logger.info("Email Submitted successfully")
    return {"type": "ok", "status": r.status_code, "info": r.text}
