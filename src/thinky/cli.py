import logging
from typing import Annotated, Union

import typer
from rich import print

from thinky._registry import agent_registry

from . import __version__
from ._project_setup import project_init
from ._registry import get_agent_imports
from ._run import run_agent
from .logging import console, setup_logging

app = typer.Typer(rich_markup_mode="rich")

logger = logging.getLogger(__name__)


def version_callback(value: bool) -> None:
    if value:
        print(f"Thinky CLI version: [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def callback(
    ctx: typer.Context,
    version: Annotated[
        Union[bool, None],
        typer.Option(
            "--version",
            "-V",
            help="Show the version and exit.",
            callback=version_callback,
        ),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Enable verbose output: INFO")
    ] = False,
    vv: Annotated[
        bool, typer.Option("-vv", help="Enable more verbose output: DEBUG")
    ] = False,
) -> None:
    """
    Thinky CLI - The [bold]thinky[/bold] command line app.

    Manage your [bold]thinky[/bold] projects, build, host and run your Agents.

    Read more in the docs: [link=https://thinky.maxscheijen.com]https://thinky.maxscheijen.com[/link].
    """

    if verbose:
        log_level = logging.INFO
    elif vv:
        log_level = logging.DEBUG
    else:
        # Disable logging
        log_level = logging.CRITICAL + 1

    setup_logging(level=log_level)

    if ctx.invoked_subcommand != "api":
        get_agent_imports()


@app.command(help="List all the available agents")
def list():
    available_agent_names = [k for k in agent_registry.keys()]

    if available_agent_names:
        print("[bold]Available Agents[/bold]:")
        for i, agent in enumerate(available_agent_names):
            number_format = f"{i + 1}."
            print(f"{number_format:<3} {agent}")
    else:
        print("[bold]No Available Agents[/bold]")


@app.command()
def run(
    agent: Annotated[str, typer.Argument(help="The name of the agent to run")],
    input: Annotated[str, typer.Argument(help="The initial input to the agent.")],
):
    """Run your agent with a given input message."""

    import asyncio

    with console.status(f"Agent '{agent}' running..."):
        result = asyncio.run(run_agent(agent, input))

    console.print(result.final_output)


@app.command()
def api(
    host: Annotated[
        str,
        typer.Option(
            help="The host to serve on. For local development use [blue]127.0.0.1[/blue]. To enable public access, e.g. in a container, use all the IP address available with [blue]0.0.0.0[/blue]."
        ),
    ] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option(
            help="The port to server on. You would normally have termination proxy on top (another program) handling HTTPS on port [blue]433[/blue], transferring the communication to your app."
        ),
    ] = 8000,
    reload: Annotated[
        bool,
        typer.Option(
            help="Reload the server when files change. Defaults to [blue]False[/false]"
        ),
    ] = False,
):
    """Host your registerd agents in a web server."""
    import uvicorn

    uvicorn.run(
        "thinky.api.main:create_app",
        host=host,
        port=port,
        reload=reload,
        workers=None,
        factory=True,
    )


@app.command()
def init():
    """Initialize and setup a new agent project."""

    name = input("What is the name of your project: ")

    with console.status(f"Setting up {name} agent project..."):
        project_init(name)
        console.print(f"Project setup `{name}` succesfull!")
        console.print(
            "Activate .venv with: [green]source[/green] [yellow].venv/bin/activate[/yellow]"
        )


def main() -> None:
    app()
