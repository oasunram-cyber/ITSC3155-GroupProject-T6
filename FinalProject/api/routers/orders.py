from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from controllers import orders as controller
from schemas import orders as schema
from dependencies.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("/", response_model=schema.Order)
def create_order(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

@router.get("/", response_model=List[schema.Order])
def read_all(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return controller.read_all(db, start_date=start_date, end_date=end_date)

@router.get("/{order_id}", response_model=schema.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, order_id)

@router.get("/tracking/{tracking_number}", response_model=schema.Order)
def get_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking_number(db, tracking_number)

@router.get("/by-date/", response_model=List[schema.Order])
def get_by_date_range(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    return controller.read_by_date_range(db, start_date, end_date)

@router.get("/revenue", response_model=schema.RevenueResponse)
def get_revenue(db: Session = Depends(get_db)):
    return controller.get_revenue(db)

@router.get("/revenue/{target_date}", response_model=schema.DailyRevenueResponse)
def get_daily_revenue(target_date: date, db: Session = Depends(get_db)):
    return controller.daily_revenue(db, target_date)

@router.put("/{order_id}", response_model=schema.Order)
def update(order_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db, order_id, request)

@router.delete("/{order_id}")
def delete(order_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, order_id)

