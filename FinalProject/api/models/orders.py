from sqlalchemy import Column, Integer, String, DateTime, Numeric, Enum, func
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
import enum


class OrderStatus(str, enum.Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=False)
    address = Column(String(255), nullable=False)

    # optional description of the order
    description = Column(String(255), nullable=True)

    order_date = Column(DateTime, server_default=func.now())
    order_status = Column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False
    )
    tracking_number = Column(String(100), unique=True, nullable=True)
    total_price = Column(Numeric(10, 2), nullable=False, default=0)

    # relationships
    order_details = relationship(
        "OrderDetail",
        back_populates="order",
        cascade="all, delete-orphan",
    )
    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
    )
    reviews = relationship(
        "Reviews",
        back_populates="order",
        cascade="all, delete-orphan",
    )
