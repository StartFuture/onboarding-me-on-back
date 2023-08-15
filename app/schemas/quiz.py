from pydantic import BaseModel, Field
from typing import Optional

link_video_pattern = r"(https\:\/\/)?www\.youtube\.com\/watch\?v\=[A-z0-9]+"
quiz_type_pattern = r"culture|principle"


class Alternative(BaseModel):
    alternative_id: Optional[int] = None
    text: str
    is_answer: int = Field(description="0 or 1", ge=0, le=1)


class Quiz(BaseModel):
    quiz_id: Optional[int] = None
    link_video: str = Field(pattern=link_video_pattern)
    score: int
    title: str
    question: str
    quiz_type: str = Field(pattern=quiz_type_pattern)
    game_id: int
    alternatives: list[Alternative]
