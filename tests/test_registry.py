import os
import tempfile
from pathlib import Path

import pytest
from agents import Agent

from thinky import agent_registry, register_agent
from thinky._registry import (
    _get_module_data_from_path,
    get_agent,
    get_agent_path,
)
from thinky.exceptions import AgentRegistrationException


@pytest.fixture()
def clear_resistry():
    agent_registry.clear()


class DummyAgent(Agent):
    def __init__(self):
        self.name = "dummy"


def test_register_agent_success(clear_resistry):
    @register_agent
    def dummy() -> Agent:
        return DummyAgent()

    assert "dummy" in agent_registry
    assert agent_registry["dummy"] == dummy
    assert isinstance(agent_registry["dummy"](), DummyAgent)


def test_register_agent_duplicate(clear_resistry):
    @register_agent
    def _() -> Agent:
        return DummyAgent()

    with pytest.raises(AgentRegistrationException) as exec_info:

        @register_agent
        def _() -> Agent:
            return DummyAgent()

        assert "already registerd" in str(exec_info)


def test_get_agent_succes(clear_resistry):
    @register_agent
    def _() -> Agent:
        return DummyAgent()

    agent = get_agent("_")
    assert isinstance(agent, DummyAgent)
    assert agent.name == "dummy"


def test_get_agent_not_registered(clear_resistry):
    with pytest.raises(AgentRegistrationException, match="not registered"):
        get_agent("unknown_agent")


def test_get_module_data_from_path():
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_dir = Path(tmp_dir) / "my" / "agents"
        test_dir.mkdir(parents=True)

        result = _get_module_data_from_path(test_dir)

        assert result.module_import_str == "my.agents"
        assert result.extra_sys_path == test_dir.parent.resolve()
        assert result.module_paths == test_dir.resolve()


def test_get_agent_path_with_argument():
    path = Path("/explicit/path")
    result = get_agent_path(path)
    assert result == path


def test_get_agent_path_from_env():
    fake_path = "/env/agent/path"
    os.environ["AGENT_DIR_PATH"] = fake_path

    result = get_agent_path()
    assert result == Path(fake_path)

    del os.environ["AGENT_DIR_PATH"]


def test_get_agent_path_env_missing():
    if "AGENT_DIR_PATH" in os.environ:
        del os.environ["AGENT_DIR_PATH"]
    with pytest.raises(RuntimeError, match="Missing required environment variable"):
        get_agent_path()
