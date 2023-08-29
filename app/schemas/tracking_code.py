from pydantic import BaseModel, Field, constr

from app import parameters

class TrackingCode(BaseModel):
    tracking_code:str = Field( pattern=parameters.dict_regex['tracking code pattern'])
    employee_id: int