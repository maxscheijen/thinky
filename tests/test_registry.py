import pytest
from agents import Agent

from thinky import agent_registry, register_agent
from thinky._registry import get_agent
from thinky.exceptions import AgentRegistrationException


class DummyAgent(Agent):
    def __init__(self):
        self.name = "dummy"


@pytest.fixture(autouse=True)
def clear_resistry():
    agent_registry.clear()


def test_register_agent():
    @register_agent
    def dummy_agent() -> Agent:
        return DummyAgent()

    assert "dummy_agent" in agent_registry
    assert agent_registry["dummy_agent"] == dummy_agent


def test_register_agent_duplicate():
    @register_agent
    def duplicate_agent() -> Agent:
        return DummyAgent()

    with pytest.raises(AgentRegistrationException) as exec_info:

        @register_agent
        def duplicate_agent() -> Agent:
            return DummyAgent()

        assert "Agent 'duplicate_agent' is already registerd." in str(exec_info)


def test_get_agent_succes():
    @register_agent
    def retrieve_agent() -> Agent:
        return DummyAgent()

    agent = get_agent("retrieve_agent")
    assert isinstance(agent, DummyAgent)
    assert agent.name == "dummy"


def test_get_agent_not_registered():
    with pytest.raises(AgentRegistrationException) as exec_info:
        get_agent("non_existing_agent")

    assert "Agent 'non_existing_agent' is not registered." in str(exec_info)
