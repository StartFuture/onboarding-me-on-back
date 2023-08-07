from pydantic import BaseModel, Field

class Enterprise(BaseModel):
    id: str
    name: str
    cnpj: str = Field(pattern=r'^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$')
    