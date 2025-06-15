import os

import pytest
from openai import AsyncAzureOpenAI

from thinky.client import client_selector


@pytest.mark.parametrize("provider", ["openai", "azure"])
def test_client_selector_valid_providers(provider):
    os.environ["PROVIDER"] = "openai"
    os.environ["OPENAI_API_KEY"] = "fake-key"
    os.environ["OPENAI_API_VERSION"] = "fake-key"
    os.environ["AZURE_OPENAI_API_KEY"] = "fake-key"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "fake-key"
    if provider == "openai":
        with pytest.raises(NotImplementedError):
            client = client_selector(provider)
        # assert isinstance(client, AsyncOpenAI)
    if provider == "azure":
        client = client_selector(provider)
        assert isinstance(client, AsyncAzureOpenAI)
