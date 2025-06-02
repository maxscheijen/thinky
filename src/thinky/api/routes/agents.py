from typing import List

from agents import Runner
from fastapi import APIRouter, HTTPException

from thinky import agent_registry, get_agent
from thinky.api import schemas
from thinky.exceptions import AgentRegistrationException

agent_router = APIRouter(prefix="/agent")


@agent_router.get("/", response_model=List[str])
async def list_agents():
    return [k for k in agent_registry.keys()]


@agent_router.post("/{agent_id}/run")
async def create_agent_run(agent_id: str, body: schemas.RunRequest):
    try:
        agent = get_agent(agent_id=agent_id)
        response = await Runner.run(agent, input=body.message)
    except AgentRegistrationException as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")

    if response.final_output is None:
        raise HTTPException(status_code=404, detail="Agent dit not return a reponse")
    return schemas.RunResponse(
        message=body.message, model=body.model, response=response.final_output
    )
