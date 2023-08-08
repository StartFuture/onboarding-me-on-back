from pydantic import BaseModel, Field
from typing import Optional

LINK_DOWNLOAD_PATTERN = r"https\:\/\/[www\.]?[A-z\.0-9]+[\.A-z]+\/.*"

class Tool(BaseModel):
    id_tool: Optional[int] = None 
    link_download: str = Field(pattern = LINK_DOWNLOAD_PATTERN)
    name: str
    score: int
    #game_id:
    #category_id: