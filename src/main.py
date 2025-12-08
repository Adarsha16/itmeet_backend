from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import os
import httpx
import google.generativeai as genai
from dotenv import load_dotenv

from context import EVENT_CONTEXT   # <-- import here

load_dotenv()

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    system_instruction=EVENT_CONTEXT
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_bot(req: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key not configured")

    try:
        response = await model.generate_content_async(req.message)
        return {"reply": response.text}

    except Exception as e:
        print(f"Gemini Error: {e}")
        raise HTTPException(status_code=500, detail="AI processing failed")