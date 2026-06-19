# src/config.py

from .env import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

TOP_K = 3

RETRIEVAL_THRESHOLD = 0.45

SENSITIVE_KEYWORDS = [
    "billing",
    "refund",
    "charge",
    "payment",
    "legal",
    "account deletion",
    "account modification"
]