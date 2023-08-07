from pydantic import BaseModel, Field


LINK_VIDEO_PATTERN = r"https\:\/\/[www\.]?[A-z\.0-9]+[\.A-z]+\/.*"
QUIZ_TYPE_PATTERN = r"culture|principle"


class Quiz(BaseModel):
    link_video: str = Field(pattern=LINK_VIDEO_PATTERN)
    score: int
    title: str
    question: str
    quiz_type: str = Field(pattern=QUIZ_TYPE_PATTERN)
    