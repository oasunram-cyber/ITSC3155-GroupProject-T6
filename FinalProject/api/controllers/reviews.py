from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import reviews as model
from schemas import reviews as schema
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request: schema.ReviewCreate):
    new_review = model.Reviews(
        order_date=request.order_date, # Note: Ensure your Schema expects this string/date
        review=request.review,
        rating=request.rating
    )
    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_review

def read_all(db: Session):
    return db.query(model.Reviews).all()

def read_one(db: Session, item_id: int):
    item = db.query(model.Reviews).filter(model.Reviews.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Review not found")
    return item

def delete(db: Session, item_id: int):
    item = db.query(model.Reviews).filter(model.Reviews.id == item_id)
    if not item.first():
        raise HTTPException(status_code=404, detail="Review not found")
    item.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Deleted"}
