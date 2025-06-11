from typing import Any, Dict, Optional

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


class RunResponse(BaseModel):
    id: int
    message: str
    response: str


class ToolItemResponse(BaseModel):
    name: str
    description: str
    meta_data: Optional[Dict[str, Any]] = None
