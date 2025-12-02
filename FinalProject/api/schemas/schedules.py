from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .accounts import accounts

class ScheduleBase(BaseModel):
    name: str
    rank: str
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str


class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    rank: Optional[str] = None
    monday: Optional[str] = None
    tuesday: Optional[str] = None
    wednesday: Optional[str] = None
    thursday: Optional[str] = None
    friday: Optional[str] = None
    saturday: Optional[str] = None
    sunday: Optional[str] = None


class Schedule(ScheduleBase):
    id: int

    class ConfigDict:
        from_attributes = True
