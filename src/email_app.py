import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby0jffnZcWz3C1BdWRb7x9A1RFihwFuthEgxAsxhYF2C9NIfo0D1WBXNYQ11XFkaGUrvg/exec"

class EmailRequest(BaseModel):
    email: str

@app.post("/submit-email")
async def submit_email(data: EmailRequest):
    # Send a POST request to Google Script
    payload = {"email": data.email}
    response = requests.post(GOOGLE_SCRIPT_URL, json=payload)

    return {
        "email_sent_to_google": data.email,
        "google_response": response.text
    }




