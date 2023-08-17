from pydantic import BaseModel
from typing import Optional

class CategoryTool(BaseModel):
    category_tool_id: Optional[int] = None
    name: str
    