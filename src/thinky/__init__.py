"""A lightweight library for building and hosting agents."""

from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from dotenv import load_dotenv

from thinky.client import ollama_client

from ._registry import agent_registry, get_agent, register_agent

load_dotenv()
set_tracing_disabled(True)

set_default_openai_client(ollama_client)
set_default_openai_api("chat_completions")


__version__ = "0.0.1"

__all__ = ["agent_registry", "get_agent", "register_agent"]
