from fastapi import APIRouter

from .agents import agent_router
from .health import health_router
from .tool import tool_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(health_router, tags=["Health"])
v1_router.include_router(agent_router, tags=["Agent"])
v1_router.include_router(tool_router, tags=["Tool"])
