from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # THIS is the only foreign key that links recipes -> sandwiches
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"), nullable=False)

    # link to resources (ingredients in inventory)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)

    # how much of this resource is used in this sandwich
    amount = Column(Integer, nullable=False)

    # relationships
    sandwich = relationship(
        "Sandwich",
        back_populates="recipes",
        primaryjoin="Recipe.sandwich_id == Sandwich.id",
    )

    resource = relationship("Resource", back_populates="recipes")
