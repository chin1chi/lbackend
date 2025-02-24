from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PartnerBase(BaseModel):
    name: str
    info: str

class PartnerCreate(PartnerBase):
    pass

class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    info: Optional[str] = None

class PartnerInDB(PartnerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PartnerOut(PartnerInDB):
    pass
