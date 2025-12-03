from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dependencies.database import Base


class Schedules(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)

    # link to Accounts via foreign key
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    monday = Column(String(100), nullable=True)
    tuesday = Column(String(100), nullable=True)
    wednesday = Column(String(100), nullable=True)
    thursday = Column(String(100), nullable=True)
    friday = Column(String(100), nullable=True)
    saturday = Column(String(100), nullable=True)
    sunday = Column(String(100), nullable=True)

    # relationship back to Accounts
    account = relationship("Accounts", back_populates="schedules")
