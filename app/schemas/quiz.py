from pydantic import BaseModel, Field


link_video_pattern = r"https\:\/\/[www\.]?[A-z\.0-9]+[\.A-z]+\/.*"
quiz_type_pattern = r"culture|principle"


class Alternative(BaseModel):
    text: str
    is_answer: int = Field(description="0 or 1", ge=0, le=1)


class Quiz(BaseModel):
    link_video: str = Field(pattern=link_video_pattern)
    score: int
    title: str
    question: str
    quiz_type: str = Field(pattern=quiz_type_pattern)
    alternatives: list[Alternative]
