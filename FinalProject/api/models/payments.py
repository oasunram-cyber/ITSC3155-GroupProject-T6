from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric, Enum, func
from sqlalchemy.orm import relationship
from dependencies.database import Base
import enum


class PaymentStatus(str, enum.Enum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"


class PaymentType(str, enum.Enum):
    CREDIT_CARD = "Credit Card"
    PAYPAL = "PayPal"
    OTHER = "Other"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to link to the order (1–1)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)

    # Use the Enum for status
    transaction_status = Column(
        Enum(PaymentStatus),
        nullable=False,
        default=PaymentStatus.PENDING,
    )

    # ID from payment processor
    transaction_id = Column(String(255), nullable=False, index=True)

    # Safe card details
    last_4_digits = Column(String(4), nullable=True)
    card_brand = Column(String(50), nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # Relationship back to Order
    order = relationship("Order", back_populates="payment")
