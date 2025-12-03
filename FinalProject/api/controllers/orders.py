from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime


from models import orders as model
from schemas import orders as schema


def create(db: Session, request: schema.OrderCreate):
    """
    Create a new order.
    """
    new_item = model.Order(
        customer_name=request.customer_name,
        phone_number=request.phone_number,   # ✅ NEW: pass phone_number
        address=request.address,             # ✅ NEW: pass address
        description=request.description,
        total_price=request.total_price,
        order_status=request.order_status,
        tracking_number=request.tracking_number,
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return new_item


def read_all(db: Session, start_date: str = None, end_date: str = None):
    query = db.query(model.Order)
    
    if start_date and end_date:
        query = query.filter(model.Order.order_date >= start_date)\
                     .filter(model.Order.order_date <= end_date)
    
    return query.all()

def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return result


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            # ✅ FIXED: 404, not 44
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Id not found!",
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return item


def update(db: Session, item_id: int, request: schema.OrderUpdate):
    try:
        item_q = db.query(model.Order).filter(model.Order.id == item_id)
        existing = item_q.first()
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Id not found!",
            )

        update_data = request.dict(exclude_unset=True)
        item_q.update(update_data, synchronize_session=False)
        db.commit()
        return item_q.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )


def delete(db: Session, item_id: int):
    try:
        item_q = db.query(model.Order).filter(model.Order.id == item_id)
        if not item_q.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Id not found!",
            )
        item_q.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Q: "How can I track the status of my order by my tracking number?"
def read_by_tracking(db: Session, tracking_number: str):
    item = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()
    if not item:
        raise HTTPException(status_code=404, detail="Tracking number not found")
    return item

# Q: "How can I determine the total revenue generated?"
def get_revenue(db: Session):
    # Sums up the 'total_price' column from all orders
    result = db.query(func.sum(model.Order.total_price)).scalar()
    return {"total_revenue": result or 0.0}



