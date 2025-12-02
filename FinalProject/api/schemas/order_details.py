from typing import Optional
from pydantic import BaseModel, ConfigDict


class OrderDetailBase(BaseModel):
    sandwich_id: int
    amount: int


class OrderDetailCreate(OrderDetailBase):
    order_id: int


class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    amount: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int
    line_price: float

    model_config = ConfigDict(from_attributes=True)
