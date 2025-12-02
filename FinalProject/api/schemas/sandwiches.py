from datetime import datetime
from typing import Optional
from pydantic import BaseModel

#This is the Menu
class SandwichBase(BaseModel):
    sandwich_name: str
    price: float
    ingredients: int
    calories: int
    category: str


class SandwichCreate(SandwichBase):
    pass


class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = None
    price: Optional[float] = None
    ingredients: Optional[int] = None
    calories: Optional[int] = None
    category: Optional[str] = None


class Sandwich(SandwichBase):
    id: int

    class ConfigDict:

        from_attributes = True

