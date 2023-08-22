from pydantic import BaseModel, Field

from app import parameters


class Company(BaseModel):
    id: int
    name: str
    cnpj: str = Field(pattern=parameters.dict_regex["cnpj pattern"])
    