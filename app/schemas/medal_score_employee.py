from pydantic import BaseModel, Field, constr


class Medal_Score_Employee(BaseModel):
    employee_id: int
    game_id: int
