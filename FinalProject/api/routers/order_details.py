from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from controllers import order_details as controller
from schemas import order_details as schema

router = APIRouter(
    prefix="/order-details",
    tags=["order_details"],
)


@router.post("/", response_model=schema.OrderDetail)
def create_order_detail(request: schema.OrderDetailCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)


@router.get("/", response_model=List[schema.OrderDetail])
def get_order_details(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{detail_id}", response_model=schema.OrderDetail)
def get_order_detail(detail_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, detail_id)


@router.put("/{detail_id}", response_model=schema.OrderDetail)
def update_order_detail(
    detail_id: int,
    request: schema.OrderDetailUpdate,
    db: Session = Depends(get_db),
):
    return controller.update(db, detail_id, request)


@router.delete("/{detail_id}")
def delete_order_detail(detail_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, detail_id)
