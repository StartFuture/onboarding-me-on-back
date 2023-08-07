from pydantic import BaseModel, Field

LINK_DOWNLOAD_PATTERN = r"https\:\/\/[www\.]?[A-z\.0-9]+[\.A-z]+\/.*"

class Tool(BaseModel):
    link_download: str = Field(pattern = LINK_DOWNLOAD_PATTERN)
    name: str
    score: int