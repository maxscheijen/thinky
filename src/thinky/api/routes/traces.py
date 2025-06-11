import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from thinky.api.db.models import AgentRun
from thinky.api.schemas import TraceResponse

from ..db.session import get_db

trace_router = APIRouter(prefix="/trace")


@trace_router.get("/{id}", response_model=TraceResponse)
def get_run_by_id(id: str, db: Session = Depends(get_db)):
    agent_run = db.query(AgentRun).filter(AgentRun.id == id).first()

    if not agent_run:
        raise HTTPException(status_code=404, detail=f"Agent run with {id} not found.")

    agent_run.steps = json.loads(str(agent_run.steps))

    return agent_run
