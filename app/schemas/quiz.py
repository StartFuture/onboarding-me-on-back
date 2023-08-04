from pydantic import BaseModel

class Quiz(BaseModel):
    link_video: str
    score: int
    title: str
    question: str
    quiz_type: str