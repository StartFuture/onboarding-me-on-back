from pydantic import BaseModel

class TrackKitCreate(BaseModel):
    employee_id: int
    welcome_kit_id: int
    tracking_code: str 
    status: str

class TrackKitEdit(BaseModel):
    tracking_code: str 
    status: str
