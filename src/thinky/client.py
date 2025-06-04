from openai import AsyncOpenAI

ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="placeholder-ollama-key",
)
