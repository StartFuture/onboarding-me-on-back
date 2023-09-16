from pydantic import BaseModel

class TrackKitCreate(BaseModel):
    employee_id: int
    welcome_kit_id: int
