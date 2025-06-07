from agents import Runner, RunResult

from thinky._registry import get_agent


async def run_agent(agent_id: str, input: str) -> RunResult:
    """
    Run a workflow starting at the given agent. The agent will run in a loop until a final
    output is generated.

    Args:
        input (str): The initial input to the agent. You can pass a single string for a user message,
        agent_id (str): The agent id (name).

    Returns:
        RunResult: A run result containing all the inputs, guardrail results and the output of the last
        agent. Agents may perform handoffs, so we don't know the specific type of the output.
    """
    agent = get_agent(agent_id=agent_id)
    response = await Runner.run(agent, input=input)
    return response
