from typing import Union, Optional

from money import Money
import pydantic
from pydantic.class_validators import validator
from pydantic.networks import HttpUrl


class Part(pydantic.BaseModel):
    reference: str
    title: str
    price: Money
    image: Optional[HttpUrl]
    available: Union[bool, None] = None
    discontinued: Union[bool, None] = None

    @validator("reference")
    def format_reference(cls, v):
        if v.count("-") != 2:
            raise ValueError("must contain 3 times character -")
        return v.upper()

    class Config:
        arbitrary_types_allowed = True
