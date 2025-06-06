from typing import Any, Dict, Optional

from pydantic import BaseModel


class RunRequest(BaseModel):
    message: str
    model: str


class RunResponse(RunRequest):
    response: str


class ToolItemResponse(BaseModel):
    name: str
    description: str
    meta_data: Optional[Dict[str, Any]] = None
