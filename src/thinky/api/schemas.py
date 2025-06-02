from pydantic import BaseModel


class RunRequest(BaseModel):
    message: str
    model: str


class RunResponse(RunRequest):
    response: str
