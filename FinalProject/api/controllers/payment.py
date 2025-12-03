from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from models import payments as model
from schemas import payments as schema


def create(db: Session, request: schema.PaymentCreate):
    """
    Create a new payment record.
    This should be called *after* a successful charge
    with a payment processor.
    """
    new_item = model.Payment(
        order_id=request.order_id,
        amount=request.amount,
        payment_type=request.payment_type,
        transaction_status=request.transaction_status,
        transaction_id=request.transaction_id,
        last_4_digits=request.last_4_digits,
        card_brand=request.card_brand,
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return new_item


def read_one(db: Session, item_id: int):
    try:
        item = (
            db.query(model.Payment)
            .filter(model.Payment.id == item_id)
            .first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Id not found!",
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return item


def read_by_order_id(db: Session, order_id: int):
    """
    Get payment details for a specific order.
    """
    try:
        item = (
            db.query(model.Payment)
            .filter(model.Payment.order_id == order_id)
            .first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found for this order",
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return item
