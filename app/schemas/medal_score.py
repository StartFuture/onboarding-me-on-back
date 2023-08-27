from pydantic import BaseModel, Field, constr


class Medal_Score(BaseModel):
    medal_id: int
    score_id: int
