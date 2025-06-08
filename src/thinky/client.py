import logging
import os
from typing import Literal, get_args

from dotenv import load_dotenv
from openai import AsyncAzureOpenAI, AsyncOpenAI

load_dotenv()

logger = logging.getLogger(__name__)

ProviderType = Literal["openai", "azure", "ollama"]
valid_providers = get_args(ProviderType)


def client_selector(provider: ProviderType) -> AsyncOpenAI:
    if provider not in valid_providers:
        raise ValueError(
            f"'{provider}' is not a valid provider. Choose one of: {valid_providers}"
        )

    if provider == "openai":
        return AsyncOpenAI()

    if provider == "azure":
        return AsyncAzureOpenAI()

    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise EnvironmentError(
            "Missing BASE_URL environment variable required for 'ollama' provider."
        )
    return AsyncOpenAI(
        base_url=base_url,
        api_key="placeholder-ollama-key",
    )


def get_client() -> AsyncOpenAI:
    provider = os.environ.get("PROVIDER")

    if not provider:
        raise ValueError(
            f"The provider must be set by setting the PROVIDER enviroment variable to one of these provider: {valid_providers}"
        )

    return client_selector(provider)  # type: ignore
