from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from controllers import payments as controller
from schemas import payments as schema
from dependencies.database import get_db

router = APIRouter(
    tags=['Payments'],
    prefix="/payments"
)

@router.post("/", response_model=schema.Payment)
def create_payment(request: schema.PaymentCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/{item_id}", response_model=schema.Payment)
def read_payment(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from controllers import payment as controller
from schemas import payments as schema

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)


@router.post("/", response_model=schema.Payment)
def create_payment(request: schema.PaymentCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)


@router.get("/{payment_id}", response_model=schema.Payment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, payment_id)


@router.get("/by-order/{order_id}", response_model=schema.Payment)
def get_payment_by_order(order_id: int, db: Session = Depends(get_db)):
    return controller.read_by_order_id(db, order_id)

