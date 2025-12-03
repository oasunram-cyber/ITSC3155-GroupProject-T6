from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(Integer, unique=True, nullable=False)
    percent = Column(DECIMAL(4, 2), nullable=False, server_default="0.0")
    expiration = Column(DateTime)
    sandwich = Column(String(100), ForeignKey("sandwiches.sandwich_name"))
    promotion = Column(String(100), unique=True)

    sandwiches = relationship("Sandwich", back_populates="promotions")

    # promo code customers will type in (e.g., "WELCOME10")
    code = Column(String(50), unique=True, nullable=False)

    # discount percent, e.g., 10.00 for 10%
    percent = Column(DECIMAL(4, 2), nullable=False, server_default="0.0")

    # optional expiration date
    expiration = Column(DateTime, nullable=True)

    # which sandwich this promotion applies to (by sandwich name)
    sandwich = Column(
        String(100),
        ForeignKey("sandwiches.sandwich_name"),
        nullable=True
    )

    # description / label for this promotion (e.g., "New user discount")
    promotion = Column(String(100), unique=True, nullable=True)

    # relationship back to Sandwich
    # NOTE: attribute name here must match back_populates in Sandwich model
    sandwich_obj = relationship(
        "Sandwich",
        back_populates="promotions",
        primaryjoin="Promotion.sandwich == Sandwich.sandwich_name",
    )
