from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import promotions as model
from ..schemas import promotions as schema
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request: schema.PromotionCreate):
    new_item = model.Promotion(
        code=request.code,
        percent=request.percent,
        expiration=request.expiration,
        sandwich=request.sandwich,
        promotion=request.promotion
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item

def read_all(db: Session):
    return db.query(model.Promotion).all()

def read_one(db: Session, item_id: int):
    item = db.query(model.Promotion).filter(model.Promotion.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return item

def update(db: Session, item_id: int, request: schema.PromotionUpdate):
    item = db.query(model.Promotion).filter(model.Promotion.id == item_id)
    if not item.first():
        raise HTTPException(status_code=404, detail="Promotion not found")
    item.update(request.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return item.first()

def delete(db: Session, item_id: int):
    item = db.query(model.Promotion).filter(model.Promotion.id == item_id)
    if not item.first():
        raise HTTPException(status_code=404, detail="Promotion not found")
    item.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Deleted"}
