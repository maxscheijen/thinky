from agents import Agent

from thinky import register_agent


@register_agent
def calc_agent():
    return Agent(name="calc_agent", model="llama3.1:latest")
