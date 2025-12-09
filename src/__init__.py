import os
from http import HTTPStatus

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .event_context import EVENT_CONTEXT

load_dotenv()

app = FastAPI()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError(
        "'GEMINI_API_KEY' not found in environment variables, it is required."
    )

genai.configure(api_key=GEMINI_API_KEY)


model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite", system_instruction=EVENT_CONTEXT
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
async def chat_bot(req: ChatRequest):
    try:
        response = await model.generate_content_async(req.message)

        return {"reply": response.text}

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"An error occured while executing Gemini: {e!r}",
        )
