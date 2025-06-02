import logging
from pathlib import Path
from typing import Annotated, Union

import typer
from rich import print

from . import __version__
from .discover import get_agents
from .logger import setup_logging

app = typer.Typer(rich_markup_mode="rich")
logger = logging.getLogger(__name__)


def version_callback(value: bool) -> None:
    if value:
        print(f"nn-agents version: [green]{__version__}[/green]")
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
    log_level = logging.DEBUG if verbose else logging.INFO

    setup_logging(level=log_level)


def _get_agents(path: Union[Path, None] = None):
    try:
        import_data = get_agents(path)
    except Exception:
        raise ValueError

    logger.debug(f"Importing from {import_data.module_data.extra_sys_path}")
    logger.debug(f"Importing module {import_data.module_data.module_import_str}")
    return import_data


@app.command()
def run(
    path: Annotated[
        Union[Path, None],
        typer.Argument(help="A path to the [green]agent[/green] directory."),
    ] = None,
):
    import_data = _get_agents(path)
    print(import_data)


@app.command()
def api(
    path: Annotated[
        Union[Path, None],
        typer.Argument(help="A path to the [green]agent[/green] directory."),
    ] = None,
    *,
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
    import_data = _get_agents(path)


def main():
    app()
