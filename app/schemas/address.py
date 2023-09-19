from pydantic import BaseModel, Field
from typing import Optional

from app.parameters import dict_regex


class Address(BaseModel):
    address_id: Optional[int] = None
    num: str
    complement: str
    zipcode: str = Field(pattern=dict_regex['zipcode pattern'])
    street: str
    district: str
    city: str
    state: str
