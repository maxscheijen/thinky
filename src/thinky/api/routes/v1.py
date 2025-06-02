from fastapi import APIRouter

from .agents import agent_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(agent_router, tags=["Agent"])
