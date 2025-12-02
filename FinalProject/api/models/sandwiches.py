from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


# This is the Menu
class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), unique=True, nullable=True)

    # price of the sandwich
    price = Column(DECIMAL(4, 2), nullable=False, server_default='0.0')

    # DO NOT make this a ForeignKey to recipes.
    # It's fine to leave this as a plain Integer for now.
    ingredients = Column(Integer, nullable=True)

    calories = Column(Integer, nullable=False, server_default="0")
    category = Column(String(100), nullable=False, server_default="Sandwich")

    # relationships
    # one sandwich -> many recipe rows
    recipes = relationship(
        "Recipe",
        back_populates="sandwich",
        primaryjoin="Sandwich.id == Recipe.sandwich_id",
    )

    # one sandwich -> many order_details
    order_details = relationship("OrderDetail", back_populates="sandwich")

    # one sandwich -> many promotions (via sandwich_name)
    promotions = relationship(
        "Promotion",
        back_populates="sandwich_obj",
        primaryjoin="Sandwich.sandwich_name == Promotion.sandwich",
    )
