from typing import List

from fastapi import APIRouter

from thinky import agent_registry
from thinky.api import schemas

tool_router = APIRouter(prefix="/tool")


@tool_router.get("/", response_model=List[schemas.ToolItemResponse])
async def list_tools(verbose: bool = False):
    tools = [func().tools for _, func in agent_registry.items()]
    tools_flatten = [x for xs in tools for x in xs]

    tool_list = []
    for tool in tools_flatten:
        if tool.name not in tool_list:
            tool_dict = {"name": tool.name, "description": tool.description or ""}
            if verbose:
                tool_dict["meta_data"] = tool.params_json_schema or {}
            tool_list.append(tool_dict)
    return tool_list
