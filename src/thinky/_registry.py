from typing import Callable, Dict

from agents import Agent

from thinky.exceptions import AgentRegistrationException

agent_registry: Dict[str, Callable[..., Agent]] = {}


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
        raise AgentRegistrationException(f"Agent '{name}' is already registered.")
    agent_registry[name] = func
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
    return agent_callable()
