import os
import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from context import EVENT_CONTEXT

load_dotenv()

router = APIRouter()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite", system_instruction=EVENT_CONTEXT
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
async def chat_bot(req: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(500, "Gemini API Key not configured")

    try:
        response = await model.generate_content_async(req.message)
        return {"reply": response.text}
    except Exception:
        raise HTTPException(500, "AI processing failed")
