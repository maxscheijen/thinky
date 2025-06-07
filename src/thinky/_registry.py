import importlib
import logging
import os
import pkgutil
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Callable, Dict, Optional, Union

from agents import Agent

from thinky.exceptions import AgentRegistrationException

agent_registry: Dict[str, Callable[..., Agent]] = {}

logger = getLogger()


def register_agent(func: Callable[..., Agent]) -> Callable[..., Agent]:  # type: ignore
    """
    Decorator to register an agent creation function in the global agent registry.

    The function name is used as the key in the registry. If a function with the same
    name is already registered, an AgentRegistrationException is raised.

    Args:
        func (Callable[..., Agent]): A callable that returns an instance of Agent.

    Returns:
        Callable[..., Agent]: The original function, unmodified.

    Raises:
        AgentRegistrationException: If an agent with the same name is already registered.
    """
    name: str = func.__name__  # type: ignore
    if name in agent_registry:
        message = f"Agent '{name}' is already registered."
        logger.error(message)
        raise AgentRegistrationException(message)

    agent_registry[name] = func
    logger.debug(f"Registerd agent '{name}'")
    return func


def get_agent(agent_id: str) -> Agent:
    """
    Retrieves and instaniate a registered agent by its identifier.

    Looks up the given `agent_id` in the global `agent_registry`, retrieves the
    corresponding agent creation function, and returns a new instance of the agent.

    Args:
        agent_id (str): The unique identifier (defaults to function name) of the registed agent.

    Returns:
        Agent: An instance of the requested OpenAI Agent.

    Raises:
        AgentRegistrationException: If no agent registered under the given `agent_id`.
    """
    if agent_id not in agent_registry:
        raise AgentRegistrationException(f"Agent '{agent_id}' is not registered.")

    agent_callable = agent_registry[agent_id]
    logger.debug(f"Get agent '{agent_id}'")
    return agent_callable()


@dataclass
class ModuleData:
    module_import_str: str
    extra_sys_path: Path
    module_paths: Path


def _get_module_data_from_path(path: Path) -> ModuleData:
    """Derives module import information from a given directory path."""
    use_path = path.resolve()
    module_str = ".".join(use_path.parts[-2:])

    return ModuleData(
        module_import_str=module_str,
        extra_sys_path=use_path.parent.resolve(),
        module_paths=use_path,
    )


def get_agent_imports(path: Union[Path, None] = None):
    """Dynamically imports all submodules from a given agent directory path.

    This function is useful for ensuring all relevant agent modules are loaded,
    which is important for registration.

    Args:
        path (Union[Path, None], optional): The base path to the agent directory.
            If None, a default path will be resolved using `_get_default_paths()`.

    Raises:
        NNAgentsCLIException: If no valid default path is found.
        Exception: If `_get_module_data_from_path` or dynamic imports fail unexpectedly.
    """

    if not path:
        path = get_agent_path()

    mod_data = _get_module_data_from_path(path)

    search_path = (
        mod_data.module_paths
        if mod_data.module_paths.is_dir()
        else mod_data.module_paths.parent
    )

    for _, module_name, _ in pkgutil.walk_packages(
        [search_path], mod_data.module_import_str + "."
    ):
        try:
            importlib.import_module(module_name)
            logging.debug(f"Imported: {module_name}")
        except (ImportError, ValueError) as e:
            logging.error(f"Import error for module '{module_name}': {e}")


def get_agent_path(path: Optional[Path] = None) -> Path:
    """Get the path to the agent directory.

    Args:
        path (Optional[Path]): Relative path to the agents directory.

    Returns:
        Path: Relative path the agents directory.
    """
    if path is None:
        path_env = os.environ.get("AGENT_DIR_PATH")
        if path_env is None:
            raise RuntimeError("Missing required environment variable: AGENT_DIR_PATH")
        else:
            path = Path(path_env)
    return path
