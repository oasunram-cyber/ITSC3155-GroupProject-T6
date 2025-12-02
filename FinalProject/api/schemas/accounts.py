from pydantic import BaseModel, EmailStr
from typing import Optional

class AccountBase(BaseModel):
    name: str
    rank: str
    email: EmailStr
    phone_number: str
    address: str

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    rank: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class AccountResponse(CustomerBase):
    id: int

    class Config:
        orm_mode = True
