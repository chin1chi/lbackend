from pydantic import BaseModel
from typing import Optional


class SwipeEventBase(BaseModel):
    player_id: int
    event_id: int
    is_like: bool


class SwipeEventCreate(SwipeEventBase):
    pass


class SwipeEventUpdate(BaseModel):
    player_id: Optional[int] = None
    event_id: Optional[int] = None
    is_like: Optional[bool] = None


class SwipeEventInDB(SwipeEventBase):
    id: int

    class Config:
        orm_mode = True


class SwipeEventOut(SwipeEventInDB):
    pass


class LikeSwipeEventRequest(BaseModel):
    is_like_event: bool


class IsLikeSwipeEventsRequest(BaseModel):
    is_like_events: bool
