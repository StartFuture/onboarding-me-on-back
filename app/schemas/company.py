from pydantic import BaseModel, Field, constr

from app import parameters


class Company(BaseModel):
    id: int
    name: str
    cnpj: str = Field(pattern=parameters.dict_regex["cnpj pattern"])
    