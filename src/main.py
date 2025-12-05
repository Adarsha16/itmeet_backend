from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import os
import httpx
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

EVENT_CONTEXT = """
You are a helpful and enthusiastic AI assistant for the "IT Meet 2025 Event".
Your goal is to answer attendee questions based strictly on the information below.

EVENT DETAILS:
- Date: November 20-26, 2025
- Location: Kathmandu University, Dhulikhel, Kavre
- Website: https://itmeet.kucc.ku.edu.np/

SCHEDULE HIGHLIGHTS:
- To be decided

FAQ:

What is IT Meet?
- IT Meet is an annual, national-level event organized by Kathmandu University Computer Club (KUCC)
 with the intent of celebrating recent achievements in information and technology,
  that brings together tech enthusiasts from all over Nepal.
 This year, IT Meet aims to continue its tradition of promoting the creative
  zeal of technical personnel, providing a premier platform to share innovative 
  ideas and compete with their peers in a variety of activities, including workshops, 
  competitions, and networking sessions.

When and where is IT Meet 2025 happinng?
IT Meet 2025 will be held at Kathmandu University, Dhulikhel, with the main event days on December 26, 2025. Various sub-events will start from Dec 20
What are the event timings?
- Event timings vary by activity. A detailed schedule will be available
 on the IT Meet social media platform closer to the event date, 
 with the main days scheduled for December 26, 2025, and sub-events beginning in December 20

Will there be transportation service available for participants?
- While IT Meet 2025 does not provide direct transportation, 
we will share information on local transportation options, 
including buses, to help participants reach Kathmandu University, Dhulikhel.

Will ther be signage to help participants find their venues?
- Yes, clear signage will be placed throughout the Kathmandu University premises
 to help participants easily locate event venues, registration desks, and other important areas.


INSTRUCTIONS:
- If the user asks something not mentioned here, apologize and say you don't have that information.
- Keep answers concise and friendly.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite", system_instruction=EVENT_CONTEXT
)

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_bot(req: ChatRequest):
    """
    Endpoint to chat with the Event AI.
    """
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key not configured")

    try:
        response = await model.generate_content_async(req.message)

        return {"reply": response.text}

    except Exception as e:
        print(f"Gemini Error: {e}")
        raise HTTPException(status_code=500, detail="AI processing failed")

