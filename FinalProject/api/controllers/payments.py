from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import payments as model
from ..models import orders as order_model  # Import Order model
from ..schemas import payments as schema
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request: schema.PaymentCreate):
    # 1. Check if the Order exists
    order = db.query(order_model.Order).filter(order_model.Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 2. Create the Payment Record
    new_payment = model.Payment(
        order_id=request.order_id,
        amount=request.amount,
        payment_type=request.payment_type,
        transaction_status=request.transaction_status,
        transaction_id=request.transaction_id,
        last_4_digits=request.last_4_digits,
        card_brand=request.card_brand
    )

    try:
        db.add(new_payment)
        
        # 3. CRITICAL: Update the Order Status to "Processing"
        # This proves the transaction was successful.
        if request.transaction_status == "Success":
            order.order_status = "Processing"
            db.add(order)

        db.commit()
        db.refresh(new_payment)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_payment

def read_one(db: Session, item_id: int):
    item = db.query(model.Payment).filter(model.Payment.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Payment not found!")
    return item
