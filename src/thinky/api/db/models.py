from sqlalchemy import Column, Integer, String

from .session import Base


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, index=True)
    session_id = Column(String, index=True)
    user_id = Column(String, index=True)
    model_id = Column(String)
    message = Column(String)
    response = Column(String)
    steps = Column(String)
