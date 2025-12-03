from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from . import orders
from . import accounts

class ReviewBase(BaseModel):
    id: str
    order_date: str
    review: str
    rating: str


class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True
