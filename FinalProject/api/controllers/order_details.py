from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError

from ..models import order_details as model
from ..models import orders as orders_model
from ..models import sandwiches as sandwiches_model
from ..models import recipes as recipes_model
from ..models import resources as resources_model

from ..schemas import order_details as schema


def _recalculate_order_total(db: Session, order_id: int) -> None:
    """Recalculate total_price for an order based on its order_details."""
    order = db.query(orders_model.Order).filter(orders_model.Order.id == order_id).first()
    if not order:
        return
    total = sum([od.line_price for od in order.order_details])
    order.total_price = total
    db.commit()
    db.refresh(order)


def create(db: Session, request: schema.OrderDetailCreate):
    # validate sandwich exists
    sandwich = (
        db.query(sandwiches_model.Sandwich)
        .filter(sandwiches_model.Sandwich.id == request.sandwich_id)
        .first()
    )
    if not sandwich:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sandwich not found!",
        )

    # check ingredients (resources) via recipes
    recipes = (
        db.query(recipes_model.Recipe)
        .filter(recipes_model.Recipe.sandwich_id == request.sandwich_id)
        .all()
    )

    for recipe in recipes:
        resource = (
            db.query(resources_model.Resource)
            .filter(resources_model.Resource.id == recipe.resource_id)
            .first()
        )
        if not resource:
            continue

        required_amount = recipe.amount * request.amount
        if resource.amount < required_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient ingredient '{resource.item}'. "
                       f"Required {required_amount}{resource.unit}, "
                       f"available {resource.amount}{resource.unit}.",
            )

    # if enough, deduct the resources
    for recipe in recipes:
        resource = (
            db.query(resources_model.Resource)
            .filter(resources_model.Resource.id == recipe.resource_id)
            .first()
        )
        if not resource:
            continue
        required_amount = recipe.amount * request.amount
        resource.amount -= required_amount

    # compute line price
    line_price = float(sandwich.price) * request.amount

    new_item = model.OrderDetail(
        order_id=request.order_id,
        sandwich_id=request.sandwich_id,
        amount=request.amount,
        line_price=line_price,
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        _recalculate_order_total(db, request.order_id)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return result


def read_one(db: Session, item_id: int):
    try:
        item = (
            db.query(model.OrderDetail)
            .filter(model.OrderDetail.id == item_id)
            .first()
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Id not found!",
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return item


def update(db: Session, item_id: int, request: schema.OrderDetailUpdate):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        current = item.first()
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Id not found!",
            )

        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()

        # recalc total for the linked order
        _recalculate_order_total(db, current.order_id)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return item.first()


def delete(db: Session, item_id: int):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        current = item.first()
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Id not found!",
            )
        order_id = current.order_id
        item.delete(synchronize_session=False)
        db.commit()
        _recalculate_order_total(db, order_id)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
