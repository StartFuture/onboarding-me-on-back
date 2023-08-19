from pydantic import BaseModel, Field, constr


class Medal(BaseModel):
    name: str
    game_id: int
    image: blob
