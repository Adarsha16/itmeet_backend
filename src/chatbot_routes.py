import os, time 
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from collections import defaultdict
from context import EVENT_CONTEXT

load_dotenv() 

router = APIRouter()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

chat_history: dict = {}
session_requests: dict = defaultdict(list)
session_last_active: dict = {}

REQ_PER_SESSION = 10
WINDOW_SEC = 60
SESSION_TIMEOUT = 1800 # Allowing 30 minutes of inactivity  

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    reply: str
    rate_limit: dict

def check_rate_limit(session_id: str) -> bool:
    now = time.time()
    session_requests[session_id] = [t for t in session_requests[session_id] if now - t < WINDOW_SEC]
    
    current_count = len(session_requests[session_id])
    
    if current_count >= REQ_PER_SESSION:
        raise HTTPException(429, "Too many requests. Wait a minute.")
    
    session_requests[session_id].append(now)
    session_last_active[session_id] = now  # Update activity

    actual_requests_used = len(session_requests[session_id])
    actual_requests_left = REQ_PER_SESSION - actual_requests_used    

    return {
        "limit": REQ_PER_SESSION,
        "used": actual_requests_used,  # Include the current request being processed
        "left": actual_requests_left,  # Subtract the current request being processed
        "window": WINDOW_SEC,
        "current_count": current_count,
        "session_id": session_id
    }
    
def cleanup_inactive_sessions():
    now = time.time()
    inactive = [sid for sid, last_active in session_last_active.items() 
                if now - last_active > SESSION_TIMEOUT]
    
    for sid in inactive:
        chat_history.pop(sid, None)
        session_requests.pop(sid, None)
        session_last_active.pop(sid, None)
    
    if inactive:
        print(f"Cleaned {len(inactive)} inactive sessions")
        
@router.post("/chat", response_model=ChatResponse)
async def chat_bot(req: ChatRequest):
    
    if not GROQ_API_KEY:
        raise HTTPException(500, "API Key not configured")
    
    rate_limit_details = check_rate_limit(req.session_id)
    
    if req.session_id not in chat_history:
        chat_history[req.session_id] = [
            {"role":"system","content":EVENT_CONTEXT}
        ]
    
    chat_history[req.session_id].append({"role": "user", "content": req.message})
    
    if len(chat_history[req.session_id]) > 40: # Message storage limit = 20 
        chat_history[req.session_id] = chat_history[req.session_id][-20:]
        
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": chat_history[req.session_id],
                "temperature": 0.7,
                "max_tokens": 1024
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(response.status_code, "AI failed")
        
        reply = response.json()["choices"][0]["message"]["content"]
        chat_history[req.session_id].append({"role": "assistant", "content": reply})
        
        return {"reply": reply,
                "rate_limit": rate_limit_details
                }

@router.delete("/chat/{session_id}")
async def clear(session_id: str):
    chat_history.pop(session_id, None)
    session_requests.pop(session_id, None)
    return {"status": "cleared"}