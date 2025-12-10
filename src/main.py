import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from email_routes import router as email_router
from chatbot_routes import router as chatbot_router, cleanup_inactive_sessions

CLEANUP_INTERVAL_SECONDS = 60

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(email_router)
app.include_router(chatbot_router)

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Application starting up...")
    
    # Launch the background cleanup task
    cleanup_task_handle = asyncio.create_task(cleanup_task()) 
    yield 
    # SHUTDOWN LOGIC
    print("Application shutting down...")
    cleanup_task_handle.cancel()
    
    try:
        await cleanup_task_handle
    except asyncio.CancelledError:
        print("Background cleanup task stopped gracefully.")
        
async def cleanup_task():
    """
    Runs the cleanup_inactive_sessions function periodically.
    """
    print(f"Starting background cleanup task. Running every {CLEANUP_INTERVAL_SECONDS} seconds.")
    while True:
        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)
        cleanup_inactive_sessions()

@app.get("/")
def read_root():
    return {"status": "Groq Chatbot API Running and Background Cleanup is Scheduled"}