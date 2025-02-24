from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PartnerUserBase(BaseModel):
    partner_id: int
    user_id: int

class PartnerUserCreate(PartnerUserBase):
    pass

class PartnerUserUpdate(BaseModel):
    partner_id: Optional[int] = None
    user_id: Optional[int] = None

class PartnerUserInDB(PartnerUserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PartnerUserOut(PartnerUserInDB):
    pass
