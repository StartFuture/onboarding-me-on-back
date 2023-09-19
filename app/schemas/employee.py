from pydantic import BaseModel, Field
from typing import Optional

from app.parameters import dict_regex


class Employee(BaseModel):
    employee_id: Optional[int] = None
    first_name: str
    surname: str
    birthdate: str = Field(pattern=dict_regex['birthdate pattern'])
    employee_role: str
    email: str = Field(pattern=dict_regex['email pattern'])
    employee_password: str
    phone_number: str = Field(pattern=dict_regex['phone number pattern'])
    cpf: str = Field(pattern=dict_regex['cpf pattern'])
    level_access: str = Field(pattern=dict_regex['level access pattern'])
    company_id: int
    address_id: int
        
    
class FeedBackEmployee(BaseModel):
    employee_id:int 
    grade: int 
    message: Optional[str] = None
    feedback_type: str = Field(pattern=dict_regex['feedback type pattern'])
