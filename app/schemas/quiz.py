from pydantic import BaseModel, Field


link_video_pattern = r"https\:\/\/[www\.]?[A-z\.0-9]+[\.A-z]+\/.*"
quiz_type_pattern = r"culture|principle"


class Quiz(BaseModel):
    link_video: str = Field(pattern=link_video_pattern)
    score: int
    title: str
    question: str
    quiz_type: str = Field(pattern=quiz_type_pattern)
    