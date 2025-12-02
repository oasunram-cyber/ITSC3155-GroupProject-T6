from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .sandwiches import Sandwich

class PromotionBase(BaseModel):
  code: int
  percent: float
  expiration: datetime
  sandwich: str
  promotion: str

class PromotionCreate(PromotionBase):
  pass

class PromotionUpdate(BaseModel):
  code: Optional[int] = None
  percent: Optional[float] = None
  expiration: Optional[datetime] = None
  sandwich: Optional[str] = None
  promotion: Optional[str] = None

class Promotion(PromotionBase):
  id: int
  sandwich: Sandwich = None
  
  class ConfigDict:
    from_attributes = True
