from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ChooseEventStatus(str, Enum):
    ongoing = "В процессе"

class ChooseEventBase(BaseModel):
    state: ChooseEventStatus = ChooseEventStatus.ongoing
    expired_at: Optional[datetime] = None

class ChooseEventCreate(ChooseEventBase):
    player_id: int
    event_id: int

class ChooseEventUpdate(BaseModel):
    state: Optional[ChooseEventStatus] = None
    expired_at: Optional[datetime] = None

class ChooseEventInDB(ChooseEventBase):
    id: int
    player_id: int
    event_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ChooseEventOut(ChooseEventInDB):
    pass
