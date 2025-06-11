from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class RunRequest(BaseModel):
    message: str
    model_id: str
    user_id: str
    session_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "What is the current weather in Amsterdam?",
                    "model_id": "gpt-4o",
                    "user_id": "1",
                    "session_id": "1",
                }
            ]
        }
    }


class RunResponse(RunRequest):
    id: int
    response: str
    steps: List[Dict]


class ToolItemResponse(BaseModel):
    name: str
    description: str
    meta_data: Optional[Dict[str, Any]] = None


class TraceResponse(BaseModel):
    id: int
    agent_id: str
    session_id: int
    user_id: int
    model_id: str
    message: str
    response: str
    steps: List[Dict]
