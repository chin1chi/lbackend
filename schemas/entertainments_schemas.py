from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EntertainmentBase(BaseModel):
    entertainment: str

class EntertainmentCreate(EntertainmentBase):
    pass

class EntertainmentUpdate(BaseModel):
    entertainment: Optional[str] = None

class EntertainmentInDB(EntertainmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class EntertainmentOut(EntertainmentInDB):
    pass
