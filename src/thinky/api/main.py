from contextlib import asynccontextmanager

from fastapi import FastAPI

from thinky._registry import get_agent_imports
from thinky.api.db.session import init_db

from .routes.v1 import v1_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Logic that needs to run before application start up."""
    init_db()
    get_agent_imports()
    yield


def create_app() -> FastAPI:
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

    app = FastAPI(lifespan=lifespan)
    app.include_router(v1_router)
    return app
