"""A lightweight library for building and hosting agents."""

from agents import set_default_openai_api, set_default_openai_client
from dotenv import load_dotenv

from ._registry import agent_registry, get_agent, register_agent
from .client import ollama_client

load_dotenv()


set_default_openai_client(ollama_client)
set_default_openai_api("chat_completions")

__version__ = "0.0.1"

__all__ = ["agent_registry", "get_agent", "register_agent"]
