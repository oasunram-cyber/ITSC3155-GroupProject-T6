from typing import List
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..controllers import orders as controller
from ..schemas import orders as schema
<<<<<<< HEAD
from ..dependencies.database import engine, get_db
from typing import Optional
#=======
#>>>>>>> cf68c60 (feat: implement orders, order details, payments + fix models and db relationships)

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", response_model=schema.Order)
def create_order(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)


@router.get("/", response_model=List[schema.Order])
def get_orders(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/revenue")
def get_revenue(db: Session = Depends(get_db)):
    return controller.get_revenue(db)

@router.get("/tracking/{tracking_number}", response_model=schema.Order)
def read_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking(db, tracking_number=tracking_number)

@router.get("/{order_id}", response_model=schema.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, order_id)


@router.put("/{order_id}", response_model=schema.Order)
def update_order(
    order_id: int,
    request: schema.OrderUpdate,
    db: Session = Depends(get_db),
):
    return controller.update(db, order_id, request)


<<<<<<< HEAD
@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.get("/", response_model=list[schema.Order])
def read_all(
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    return controller.read_all(db, start_date=start_date, end_date=end_date)
=======
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, order_id)


@router.get("/tracking/{tracking_number}", response_model=schema.Order)
def get_order_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking_number(db, tracking_number)


@router.get("/by-date/", response_model=List[schema.Order])
def get_orders_by_date_range(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    return controller.read_by_date_range(db, start_date, end_date)


@router.get("/revenue/{target_date}", response_model=schema.DailyRevenueResponse)
def get_daily_revenue(target_date: date, db: Session = Depends(get_db)):
    return controller.daily_revenue(db, target_date)
#>>>>>>> cf68c60 (feat: implement orders, order details, payments + fix models and db relationships)

