import os

import pytest
from openai import AsyncAzureOpenAI, AsyncOpenAI

from thinky.client import client_selector


@pytest.mark.parametrize("provider", ["openai", "azure"])
def test_client_selector_valid_providers(provider):
    os.environ["PROVIDER"] = "openai"
    os.environ["OPENAI_API_KEY"] = "fake-key"
    os.environ["OPENAI_API_VERSION"] = "fake-key"
    os.environ["AZURE_OPENAI_API_KEY"] = "fake-key"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "fake-key"
    client = client_selector(provider)
    if provider == "openai":
        assert isinstance(client, AsyncOpenAI)
    if provider == "azure":
        assert isinstance(client, AsyncAzureOpenAI)
