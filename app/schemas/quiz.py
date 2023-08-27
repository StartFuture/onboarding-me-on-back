from pydantic import BaseModel, Field
from typing import Optional

from app import parameters

class EmployeeAlternative(BaseModel):
    employee_id: int
    alternative_id: int
    

class Alternative(BaseModel):
    alternative_id: Optional[int] = None
    text: str
    is_answer: int = Field(description="0 or 1", ge=0, le=1)


class Quiz(BaseModel):
    quiz_id: Optional[int] = None
    link_video: str = Field(pattern=parameters.dict_regex["link video pattern"])
    score: int
    title: str
    question: str
    quiz_type: str = Field(pattern=parameters.dict_regex["quiz type pattern"])
    game_id: int
    alternatives: list[Alternative]
