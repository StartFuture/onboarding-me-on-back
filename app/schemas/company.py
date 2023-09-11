from pydantic import BaseModel, Field
from typing import Optional

from app import parameters


class Company(BaseModel):
    company_id: Optional[int] = None
    name: str
    trading_name: str
    logo: str
    cnpj: str = Field(pattern=parameters.dict_regex["cnpj pattern"])
    email: str = Field(pattern=parameters.dict_regex["email pattern"])
    password: str
    state_register: str
    
