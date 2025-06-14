# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Automatically load variables from .env

# Securely access Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")
