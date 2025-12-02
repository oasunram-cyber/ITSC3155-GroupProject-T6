from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import sandwiches as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_item = model.Sandwich(
        sandwich_name=request.sandwich_name,
        price=request.price,
        calories=request.calories,
        category=request.category,
        ingredients=request.ingredients
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
    return db.query(model.Sandwich).all()

def read_one(db: Session, item_id: int):
    item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found!")
    return item

def update(db: Session, item_id: int, request):
    item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found!")
    
    item.update(request.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return item.first()

def delete(db: Session, item_id: int):
    item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found!")
    
    item.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Deleted"}

# Q: "Is there a feature that allows me to search for specific types of food?"
def search(db: Session, search_term: str):
    # Searches for sandwiches where the name contains the search term (case insensitive)
    return db.query(model.Sandwich).filter(model.Sandwich.sandwich_name.contains(search_term)).all()
