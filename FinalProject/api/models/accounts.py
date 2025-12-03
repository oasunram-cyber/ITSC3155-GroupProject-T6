from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dependencies.database import Base


class Accounts(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    rank = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)

    # One account can have many schedules
    schedules = relationship("Schedules", back_populates="account")
