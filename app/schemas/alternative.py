from pydantic import BaseModel

class Alternative(BaseModel):
    text: str
    is_answer: int
