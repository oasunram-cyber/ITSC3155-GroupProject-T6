from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime
import enum


class PaymentStatus(str, enum.Enum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"


class PaymentType(str, enum.Enum):
    CREDIT_CARD = "Credit Card"
    PAYPAL = "PayPal"
    OTHER = "Other"


class PaymentBase(BaseModel):
    payment_type: PaymentType = PaymentType.CREDIT_CARD
    transaction_status: PaymentStatus = PaymentStatus.PENDING

    # ID from payment processor
    transaction_id: str

    amount: Decimal
    last_4_digits: Optional[str] = None
    card_brand: Optional[str] = None


class PaymentCreate(PaymentBase):
    order_id: int


class Payment(PaymentBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
