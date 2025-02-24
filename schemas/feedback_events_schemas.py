from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FeedbackEventBase(BaseModel):
    is_liked: bool
    comment: Optional[str] = None
    photo: Optional[str] = None

class FeedbackEventCreate(FeedbackEventBase):
    player_id: int
    history_event_id: int

class FeedbackEventUpdate(BaseModel):
    is_liked: Optional[bool] = None
    comment: Optional[str] = None
    photo: Optional[str] = None

class FeedbackEventInDB(FeedbackEventBase):
    id: int
    player_id: int
    history_event_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class FeedbackEventOut(FeedbackEventInDB):
    pass
