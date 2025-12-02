from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict

from .order_details import OrderDetail
from .payments import Payment


class OrderStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderBase(BaseModel):
    customer_name: str
    phone_number: str
    address: str

    description: Optional[str] = None
    total_price: Decimal

    order_status: OrderStatus = OrderStatus.PENDING
    tracking_number: Optional[str] = None


class OrderCreate(OrderBase):
    # for now same as base; order_details added via separate endpoint
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

    description: Optional[str] = None
    total_price: Optional[Decimal] = None
    order_status: Optional[OrderStatus] = None
    tracking_number: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: List[OrderDetail] = []
    payment: Optional[Payment] = None

    model_config = ConfigDict(from_attributes=True)


# helpers for queries

class OrderDateRangeFilter(BaseModel):
    start_date: date
    end_date: date


class DailyRevenueResponse(BaseModel):
    date: date
    total_revenue: Decimal
