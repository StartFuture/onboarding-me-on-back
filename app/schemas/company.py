from pydantic import BaseModel, Field

from app import parameters


class Company(BaseModel):
    name: str
    trading_name: str
    logo: str
    cnpj: str = Field(pattern=parameters.dict_regex["cnpj pattern"])
    email: str = Field(pattern=parameters.dict_regex["email pattern"])
    password: str
    state_register: str
    
