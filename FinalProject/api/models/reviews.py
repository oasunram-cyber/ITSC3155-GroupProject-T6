from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dependencies.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from dependencies.database import Base



class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    review = Column(String(300))
    rating = Column(String(10))

    orders = relationship("Order", back_populates="reviews")


    # Link each review to an order
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    # Up to 300 chars of review text
    review = Column(String(300), nullable=True)

    # Numerical rating, e.g. 1–5
    rating = Column(Integer, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationship back to the Order model
    order = relationship("Order", back_populates="reviews")
