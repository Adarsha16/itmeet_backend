import os
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

GOOGLE_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL")


class EmailRequest(BaseModel):
    email: str


@router.post("/submit-email")
async def submit_email(data: EmailRequest):
    payload = {"email": data.email}
    response = requests.post(GOOGLE_SCRIPT_URL, json=payload)

    return {
        "email_sent_to_google": data.email,
        "google_response": response.text,
    }
