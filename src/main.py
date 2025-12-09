from fastapi import FastAPI
from email_routes import router as email_router
from chatbot_routes import router as chatbot_router

app = FastAPI()

app.include_router(email_router)
app.include_router(chatbot_router)
