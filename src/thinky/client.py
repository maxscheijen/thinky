import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

BASE_URL = os.environ.get("BASE_URL", "http://localhost:11434/v1")

ollama_client = AsyncOpenAI(
    base_url=os.environ.get("BASE_URL", "http://localhost:11434/v1"),
    api_key="placeholder-ollama-key",
)
