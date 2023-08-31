from pydantic import BaseModel


class Medal_Score(BaseModel):
    medal_id: int
    score_id: int
