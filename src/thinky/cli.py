import logging

import click
from rich import print

from thinky._registry import agent_registry

from . import __version__
from ._run import run_agent
from .logging import console, setup_logging

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", "-v", help="Enable verbose output: INFO")
@click.option("-vv", help="Enable more verbose output: DEBUG")
def cli(verbose: str, vv: str) -> None:
    """Thinky CLI - The thinky command line app. Manage your thinky projects, build, host and run your Agents."""
    if verbose:
        log_level = logging.INFO
    elif vv:
        log_level = logging.DEBUG
    else:
        # Disable logging
        log_level = logging.CRITICAL + 1

    setup_logging(level=log_level)


@cli.command()
def list():
    """List all the available agents"""
    available_agent_names = [k for k in agent_registry.keys()]

    if available_agent_names:
        print("[bold]Available Agents[/bold]:")
        for i, agent in enumerate(available_agent_names):
            number_format = f"{i + 1}."
            print(f"{number_format:<3} {agent}")
    else:
        print("[bold]No Available Agents[/bold]")


@cli.command()
@click.argument("The name of the agent to run")
@click.argument("The inital input to the agent.")
def run(agent: str, input: str):
    """Run your agent with a given input message."""

    import asyncio

    with console.status(f"Agent '{agent}' running..."):
        result = asyncio.run(run_agent(agent, input))

    console.print(result.final_output)


# @cli.command()
# def api(
#     host: Annotated[
#         str,
#         typer.Option(
#             help="The host to serve on. For local development use [blue]127.0.0.1[/blue]. To enable public access, e.g. in a container, use all the IP address available with [blue]0.0.0.0[/blue]."
#         ),
#     ] = "127.0.0.1",
#     port: Annotated[
#         int,
#         typer.Option(
#             help="The port to server on. You would normally have termination proxy on top (another program) handling HTTPS on port [blue]433[/blue], transferring the communication to your app."
#         ),
#     ] = 8000,
#     reload: Annotated[
#         bool,
#         typer.Option(
#             help="Reload the server when files change. Defaults to [blue]False[/false]"
#         ),
#     ] = False,
# ):
#     """Host your registerd agents in a web server."""
#     import uvicorn
#
#     uvicorn.run(
#         "thinky.api.main:create_app",
#         host=host,
#         port=port,
#         reload=reload,
#         workers=None,
#         factory=True,
#     )
#
#
# @app.command()
# def init():
#     """Initialize and setup a new agent project."""
#
#     name = input("What is the name of your project: ")
#
#     with console.status(f"Setting up {name} agent project..."):
#         project_init(name)
#         console.print(f"Project setup `{name}` succesfull!")
#         console.print(
#             "Activate .venv with: [green]source[/green] [yellow].venv/bin/activate[/yellow]"
#         )
#


def main() -> None:
    cli()
