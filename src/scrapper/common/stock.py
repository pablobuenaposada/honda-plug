from typing import Optional, Union

import pydantic
from money import Money
from pydantic.class_validators import validator
from pydantic.networks import HttpUrl


class Stock(pydantic.BaseModel):
    reference: str
    title: str
    price: Money
    image: Optional[HttpUrl]
    available: Union[bool, None] = None
    discontinued: Union[bool, None] = None
    url: HttpUrl

    @validator("reference")
    def format_reference(cls, v):
        if not 0 < v.count("-") < 3:
            raise ValueError("must contain 2 or 3 times character -")
        return v.upper()

    class Config:
        arbitrary_types_allowed = True
