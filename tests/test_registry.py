import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from agents import Agent

from thinky import agent_registry, register_agent
from thinky._registry import (
    ModuleData,
    _get_module_data_from_path,
    get_agent,
    get_agent_path,
)
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


def test_get_module_data_from_path():
    with tempfile.TemporaryDirectory() as tmp_dir:
        base_path = Path(tmp_dir)
        pkg_path = base_path / "pkg"
        mod_path = pkg_path / "mod"
        mod_path.mkdir(parents=True)

        result = _get_module_data_from_path(mod_path)
        expected_module_str = "pkg.mod"
        expected_extra_sys_path = mod_path.parent.resolve()
        expected_module_paths = mod_path.resolve()

        assert isinstance(result, ModuleData)
        assert result.module_import_str == expected_module_str
        assert result.extra_sys_path == expected_extra_sys_path
        assert result.module_paths == expected_module_paths


def test_get_agent_path_with_provided_path():
    test_path = Path("/user/test/path")
    result = get_agent_path(test_path)
    assert result == test_path, f"Expected {test_path}, but got {result}"


@patch.dict(os.environ, {"AGENT_DIR_PATH": "/env/some/path"})
def test_get_agent_path_with_env_var_set():
    result = get_agent_path()
    expected_path = Path("/env/some/path")
    assert result == expected_path, f"Expected {expected_path}, but got {result}"


@patch.dict(os.environ, {}, clear=True)
def test_get_agent_path_with_missing_env_var():
    with pytest.raises(
        RuntimeError, match="Missing required environment variable: AGENT_DIR_PATH"
    ):
        get_agent_path()
