# config.py
import os
from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Set OPENROUTER_API_KEY in .env")

EMBEDDING_MODEL = "text-embedding-3-small"   # Best free embedding for technical text
LLM_MODEL = "anthropic/claude-3-haiku"              # Excellent at reading tables, free on OpenRouter

TOP_K = 4