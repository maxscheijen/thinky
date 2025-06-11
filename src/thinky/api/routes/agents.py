import json
from typing import List

from agents import Runner
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from thinky import agent_registry, get_agent
from thinky.api import schemas
from thinky.api.db.models import AgentRun
from thinky.api.db.session import get_db
from thinky.exceptions import AgentRegistrationException

agent_router = APIRouter(prefix="/agent")


@agent_router.get("/", response_model=List[str])
async def list_agents():
    """List all the available registered."""

    return [k for k in agent_registry.keys()]


@agent_router.post("/{agent_id}/run")
async def create_agent_run(
    agent_id: str, body: schemas.RunRequest, db: Session = Depends(get_db)
):
    """Run an agent based on agent id."""

    try:
        agent = get_agent(agent_id=agent_id)
        response = await Runner.run(agent, input=body.message)

        agent_run_db = AgentRun(
            agent_id=agent_id,
            **body.model_dump(),
            response=response.final_output,
            steps=json.dumps(response.to_input_list()),
        )

        db.add(agent_run_db)
        db.commit()
        db.flush()
        db.refresh(agent_run_db)

        agent_run_db.steps = json.loads(str(agent_run_db.steps))
        return agent_run_db
    except AgentRegistrationException as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
