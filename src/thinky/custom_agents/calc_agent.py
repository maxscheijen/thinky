from agents import Agent

from thinky import register_agent
from thinky.tools import add_numbers


@register_agent
def calc_agent():
    return Agent(name="calc_agent", tools=[add_numbers])
