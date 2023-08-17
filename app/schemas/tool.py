from pydantic import BaseModel, Field
from typing import Optional

from app import parameters

class Tool(BaseModel):
    id_tool: Optional[int] = None 
    link_download: str = Field(pattern = parameters.dict_regex["link download pattern"])
    name: str = Field(pattern=parameters.dict_regex["name pattern"])
    score: int
    game_id: int
    category_id: int

class EmployeeTool(BaseModel):
    employee_tool_id: Optional[int] = None
    employee_id: int
    tool_id: int
    nick_name: str