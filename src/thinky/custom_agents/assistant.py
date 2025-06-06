from typing import TypedDict

from agents import Agent, function_tool

from thinky import register_agent


class Location(TypedDict):
    lat: float
    long: float


@function_tool
async def fetch_weather(location: Location) -> str:
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    return "sunny"


@register_agent
def assistant():
    return Agent(name="assistant", model="llama3.1:latest", tools=[fetch_weather])
