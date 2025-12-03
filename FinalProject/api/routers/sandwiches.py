from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from controllers import sandwiches as controller
from schemas import sandwiches as schema
from dependencies.database import get_db

router = APIRouter(
    prefix="/sandwiches",
    tags=["sandwiches"],
)

@router.post("/", response_model=schema.Sandwich)
def create(request: schema.SandwichCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

@router.get("/", response_model=list[schema.Sandwich])
def read_all(search: Optional[str] = None, db: Session = Depends(get_db)):
    if search:
        return controller.search(db, search)
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.Sandwich)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)

@router.put("/{item_id}", response_model=schema.Sandwich)
def update(item_id: int, request: schema.SandwichUpdate, db: Session = Depends(get_db)):
    return controller.update(db, request, item_id)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)
