import logging
from typing import Annotated, Union

import typer
from rich import print
from rich.console import Console

from . import __version__
from ._discover import get_agent_imports
from ._run import run_agent
from .logger import setup_logging

app = typer.Typer(rich_markup_mode="rich")
logger = logging.getLogger(__name__)
console = Console()

get_agent_imports()


def version_callback(value: bool) -> None:
    if value:
        print(f"thinky version: [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        Union[bool, None],
        typer.Option(
            "--version", help="Show the version and exit.", callback=version_callback
        ),
    ] = None,
    verbose: bool = typer.Option(False, help="Enable verbose output"),
) -> None:
    """
    Thinky CLI - The [bold]nn-agents[/bold] command line app.

    Manage your [bold]thinky[/bold] projects, run your agents, api, and more.

    Read more in the docs: [link=https://fastapi.tiangolo.com/fastapi-cli/]https://fastapi.tiangolo.com/fastapi-cli/[/link].
    """

    log_level = logging.DEBUG if verbose else logging.INFO

    setup_logging(level=log_level)


@app.command(help="List all the available agents")
def list():
    from thinky._registry import agent_registry

    available_agent_names = [k for k in agent_registry.keys()]
    for agent in available_agent_names:
        print(f"- {agent}")


@app.command()
def run(
    agent: Annotated[str, typer.Argument(help="The name of the agent to run")],
    input: Annotated[str, typer.Argument(help="The initial input to the agent.")],
):
    import asyncio

    with console.status(f"Agent '{agent}' running..."):
        result = asyncio.run(run_agent(agent, input))

    console.print(result.final_output)


@app.command()
def api(
    host: Annotated[
        str,
        typer.Option(
            help="The host to server on. For local development use [blue]127.0.0.1[/blue]. To enable public access, e.g. in a container, use all the IP address available with [blue]0.0.0.0[/blue]."
        ),
    ] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option(
            help="The port to server on. You would normally have termination proxy on top (another program) handling HTTPS on port [blue]433[/blue], transferring the communication to your app."
        ),
    ] = 8000,
):
    import uvicorn

    uvicorn.run(
        "thinky.api.main:create_app",
        host=host,
        port=port,
        reload=True,
        workers=None,
        factory=True,
    )


def main():
    app()
