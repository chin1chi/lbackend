from pydantic import BaseModel, constr, condate
from typing import List, Optional
from datetime import datetime

#
class UserBase(BaseModel):
    username: constr(min_length=1)  #
    phone_number: constr(regex=r'^\d{12}$')


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[constr(min_length=1)] = None
    phone_number: constr(regex=r'^\d{12}$') = None

    class Config:
        orm_mode = True
