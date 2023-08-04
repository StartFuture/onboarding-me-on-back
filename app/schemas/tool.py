from pydantic import BaseModel

class Tool(BaseModel):
    link_download: str
    name: str
    score: int