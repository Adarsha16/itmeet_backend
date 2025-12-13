import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
