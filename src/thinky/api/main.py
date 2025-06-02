import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI

from thinky._discover import get_agent_imports

from .routes.v1 import v1_router

AGENT_DIR_PATH = "AGENT_DIR_PATH"


def create_app(path: Optional[Path] = None) -> FastAPI:
    """Create and configure the FastAPI application.

    If no path is provided, attempts to load the agent directory path from
    the `AGENT_DIR_PATH` environment variable.

    Args:
        path (Optional[Path]): Optional path to the agent directory. If not provided,
            the environment variable `AGENT_DIR_PATH` must be set. Defaults to None.

    Returns:
        FastAPI: The configured FastAPI app instance.

    Raises:
        RuntimeError: If `path` is not provided and `AGENT_DIR_PATH` is not set.
    """
    if path is None:
        path_str = os.environ.get(AGENT_DIR_PATH)
        if path_str is None:
            raise RuntimeError(
                f"Missing required environment variable: {AGENT_DIR_PATH}"
            )
        else:
            path = Path(path_str)

    get_agent_imports(path)

    app = FastAPI()
    app.include_router(v1_router)
    return app
