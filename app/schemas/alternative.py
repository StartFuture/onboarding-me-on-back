from pydantic import BaseModel, Field

class Alternative(BaseModel):
    text: str
    is_answer: int = Field(description="0 or 1", ge=0, le=1)